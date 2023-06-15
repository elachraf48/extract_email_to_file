# Connect to Office 365 using admin credentials
$Username = "khalidggm77@21jq81.onmicrosoft.com"
$Password = ConvertTo-SecureString "puAMN3litzyW9p4?3C" -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential($Username, $Password)
Connect-MsolService -Credential $Credential

# Add the domain
$DomainName = "achraf.email"
$Domain = Get-MsolDomain -DomainName $DomainName
if (!$Domain) {
    $Domain = New-MsolDomain -Name $DomainName
    $Output = "Domain '$DomainName' added successfully."
} else {
    $Output = "Domain '$DomainName' already exists."
}

# Retrieve the TXT record value
$TxtValue = (Resolve-DnsName -Name $DomainName -Type TXT).Strings

# Output the result to a text file
$OutputFilePath = ".\output.txt"
$Output += "`nTXT Value: $TxtValue"
$Output | Out-File -FilePath $OutputFilePath

Write-Host "Domain: $DomainName"
Write-Host "TXT Value: $TxtValue"