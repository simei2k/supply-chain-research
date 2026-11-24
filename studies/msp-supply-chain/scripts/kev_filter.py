import pandas as pd, re, sys
df=pd.read_csv(sys.argv[1])
txt=(df.vendorProject+' '+df['product']+' '+df.vulnerabilityName+' '+df.shortDescription.fillna('')).str.lower()
cats={
 'rmm_mgmt':r'screenconnect|kaseya|\bvsa\b|simplehelp|n-able|n-central|take control|atera|ninja|datto|connectwise automate|automate|endpoint central|desktop central|endpoint manager|\bepm\b|kace|pdq|pulseway|syncro|tactical rmm|solarwinds orion|landesk|meshcentral',
 'remote_access':r'anydesk|teamviewer|remote support|privileged remote access|beyondtrust|splashtop|goto|logmein|realvnc|rustdesk|remote desktop gateway|remote access',
 'backup_secmgmt':r'veeam|commvault|veritas|acronis|arcserve|nakivo|cohesity|rubrik|backup|forticlient ems|apex one|apex central|sophos|eset|sentinelone|trend micro|kaspersky|symantec endpoint|mcafee epolicy',
 'psa_helpdesk':r'servicedesk|web help desk|sysaid|freshservice|autotask|connectwise manage|helpdesk|help desk',
 'identity':r'okta|entra|azure ad|ping identity|pingfederate|cyberark|jumpcloud|onelogin|adfs|active directory federation',
 'supply_chain_flag':r'supply chain|embedded malicious|malicious code|backdoor|trojan',
}
for c,p in cats.items(): df[c]=txt.str.contains(p,regex=True)
df['any']=df[list(cats)].any(axis=1)
sel=df[df['any']].copy()
sel['year']=sel.dateAdded.str[:4]
print(len(sel))
print(sel[list(cats)].sum())
print(pd.crosstab(sel.year, sel.knownRansomwareCampaignUse))
cols=['cveID','vendorProject','product','dateAdded','knownRansomwareCampaignUse']+list(cats)
sel.sort_values('dateAdded')[cols+['vulnerabilityName']].to_csv(sys.argv[2] if len(sys.argv)>2 else 'kev_msp_candidates.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_rows',500); pd.set_option('display.max_colwidth',60)
print(sel.sort_values('dateAdded')[['cveID','vendorProject','product','dateAdded','knownRansomwareCampaignUse']].to_string())
