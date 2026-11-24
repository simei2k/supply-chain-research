import pandas as pd, sys
df=pd.read_csv(sys.argv[1])
vp=(df.vendorProject+' | '+df['product']).str.lower()
rules=[
 # (pattern, trust boundary, subtype)
 (r'kaseya', 'RMM or management platform','RMM'),
 (r'n-able \| n-c', 'RMM or management platform','RMM'),
 (r'ivanti \| endpoint manager \(epm\)|ivanti \| endpoint manager cloud', 'RMM or management platform','Endpoint management'),
 (r'ivanti \| endpoint manager mobile|mobileiron', 'RMM or management platform','MDM'),
 (r'zoho \| desktop central|endpoint central', 'RMM or management platform','Endpoint management'),
 (r'zoho \| manageengine$', 'RMM or management platform','Endpoint management (unspecified ManageEngine)'),
 (r'quest \| kace', 'RMM or management platform','Endpoint management'),
 (r'solarwinds \| orion', 'RMM or management platform','IT monitoring'),
 (r'motex \| lanscope', 'RMM or management platform','Endpoint management'),
 (r'servicedesk plus|web help desk|sysaid', 'RMM or management platform','PSA or help desk'),
 (r'screenconnect|simplehelp|beyondtrust|teamviewer', 'Remote-access tool','Remote support'),
 (r'veeam|veritas \| backup|arcserve|nakivo|commvault|acronis', 'Backup or security-management platform','Backup'),
 (r'trend micro \| (apex|officescan)|forticlient ems', 'Backup or security-management platform','Security management'),
 (r'active directory federation', 'Identity provider','Federation'),
 (r'tj-actions|reviewdog|trivy', 'Build or release pipeline','CI/CD component'),
 (r'asus \| live update|daemon \| daemon tools', 'Software update mechanism','Trojanized update or installer'),
 (r'prettier|nx \| nx console|3cx', 'Plugin, extension or package','Package or extension'),
]
import re
out=[]
for i,r in df.iterrows():
    s=vp[i]
    for p,tb,sub in rules:
        if re.search(p,s):
            out.append(dict(cveID=r.cveID,vendor=r.vendorProject,product=r['product'],dateAdded=r.dateAdded,ransomware=r.knownRansomwareCampaignUse,trust_boundary=tb,subtype=sub,name=r.vulnerabilityName,desc=r.shortDescription));break
o=pd.DataFrame(out).sort_values('dateAdded')
o=o[o.dateAdded>='2021-01-01']
o.to_csv(sys.argv[2] if len(sys.argv)>2 else 'kev_msp_clean.csv',index=False)
print(len(o)); print(o.trust_boundary.value_counts()); print(o.groupby('trust_boundary').ransomware.apply(lambda s:(s=='Known').sum()))
pd.set_option('display.width',250);pd.set_option('display.max_rows',300)
print(o[['cveID','vendor','product','dateAdded','ransomware','subtype']].to_string(index=False))
# check 3CX, xz
print(df[df.vendorProject.str.contains('3CX|xz|Tukaani|Notepad|Polyfill',case=False)][['cveID','vendorProject','product','dateAdded']])
