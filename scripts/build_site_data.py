# Regenerates assets/data.js from the project datasets.
# Usage: python scripts/build_site_data.py . assets/data.js
import pandas as pd, json, sys, openpyxl
r=sys.argv[1]; out={}
R=lambda x,n=1: round(float(x),n)
# churn
c=pd.read_csv(f"{r}/customer-churn-analysis/telco_churn_raw.csv"); c['ch']=c.Churn.eq('Yes')
c['Tenure']=pd.cut(c.tenure,[-1,12,24,48,100],labels=['0-12 mo','13-24 mo','25-48 mo','49+ mo']).astype(str)
svc=['PhoneService','MultipleLines','OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies']
c['n']=c[svc].eq('Yes').sum(axis=1); c['Services']=c.n.clip(upper=6).map(lambda v: f"{v}+" if v==6 else str(v))
dims={}
for d in ['Contract','InternetService','PaymentMethod','Tenure','Services']:
    g=c.groupby(d).agg(rate=('ch','mean'),n=('ch','size')).reset_index()
    if d=='Services': g=g.sort_values(d)
    dims[d]={'labels':g[d].tolist(),'rate':[R(x*100) for x in g.rate],'n':g.n.tolist()}
out['churn']={'n':len(c),'rate':R(c.ch.mean()*100),'dims':dims,
 'mtm':{'n':int((c.Contract=='Month-to-month').sum()),'charge':R(c[c.Contract=='Month-to-month'].MonthlyCharges.mean(),2),'rate':R(c[c.Contract=='Month-to-month'].ch.mean()*100),'annual':R(c[c.Contract=='One year'].ch.mean()*100)},'charges':{'churned':R(c[c.ch].MonthlyCharges.mean(),2),'stayed':R(c[~c.ch].MonthlyCharges.mean(),2)}}
# jobs
j=pd.read_csv(f"{r}/job-market-analysis/job_postings_2025.csv")
s=j.assign(skill=j.skills_required.str.split(', ')).explode('skill')
sk=s.groupby('skill').agg(count=('job_id','size'),salary=('salary_usd','mean')).reset_index()
pay=sk[sk['count']>=50].sort_values('salary',ascending=False).head(12)
dem=sk.sort_values('count',ascending=False).head(12)
exp=j.groupby('experience_level').salary_usd.mean().sort_values()
wt=j.groupby('work_type').agg(sal=('salary_usd','mean'),app=('applicants','mean')).reset_index()
title=j.groupby('job_title').salary_usd.mean().sort_values(ascending=False)
out['jobs']={'n':len(j),
 'paying':{'labels':pay.skill.tolist(),'values':[round(x) for x in pay.salary]},
 'demand':{'labels':dem.skill.tolist(),'values':dem['count'].tolist()},
 'experience':{'labels':exp.index.tolist(),'values':[round(x) for x in exp]},
 'title':{'labels':title.index.tolist(),'values':[round(x) for x in title]},
 'worktype':{'labels':wt.work_type.tolist(),'salary':[round(x) for x in wt.sal],'applicants':[R(x) for x in wt.app]}}
# marketing
m=pd.read_csv(f"{r}/marketing-campaign-analysis/data/processed/marketing_segmented.csv")
g=m.groupby('RFM_Segment').agg(n=('Income','size'),spend=('MntTotal','mean'),resp=('Response','mean'),inc=('Income','mean')).sort_values('spend',ascending=False).reset_index()
ch=m[['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum()
cmp=[R(m[f'AcceptedCmp{i}'].mean()*100) for i in range(1,6)]+[R(m.Response.mean()*100)]
st=pd.read_csv(f"{r}/marketing-campaign-analysis/report/statistical_results.csv")
pts=m.sample(400,random_state=1)[['Income','MntTotal','Response']]
out['marketing']={'n':len(m),
 'revshare':None,'segments':{'labels':g.RFM_Segment.tolist(),'n':g.n.tolist(),'spend':[round(x) for x in g.spend],'resp':[R(x*100) for x in g.resp],'income':[round(x) for x in g.inc]},
 'channels':{'labels':['Web','Catalog','Store'],'values':[int(x) for x in ch]},
 'campaigns':{'labels':['Cmp 1','Cmp 2','Cmp 3','Cmp 4','Cmp 5','Last'],'values':cmp},
 'segrev':[R(x) for x in (m.groupby('RFM_Segment').MntTotal.sum()/m.MntTotal.sum()*100).reindex(g.RFM_Segment)],'scatter':[[int(a),int(b),int(c_)] for a,b,c_ in pts.values],
 'tests':st[['Test Name','Statistic','P-Value','Effect Size','Significant']].fillna('').astype(str).values.tolist()}
# books
b=pd.read_csv(f"{r}/book_scraper/fiction_books.csv",encoding='utf-8')
b['p']=b.Price.str.replace('Â','').str.replace('£','').astype(float)
bins=[10,20,30,40,50,60]; h=pd.cut(b.p,bins).value_counts().sort_index()
out['books']={'n':len(b),'avg':R(b.p.mean(),2),'labels':[f"£{int(i.left)}-{int(i.right)}" for i in h.index],'values':h.tolist(),
 'instock':int(b.Availability.str.contains('In stock').sum())}
open(sys.argv[2],'w').write('window.PORTFOLIO_DATA='+json.dumps(out,separators=(',',':'))+';\n')
print(out['churn']['mtm'], out['marketing']['segrev'], out['jobs']['experience'])
