$date = Get-Date -Format "yyyy-MM-dd_HH.mm.ss"

$OUpath = "OU=Users,OU=Internal,DC=contoso,DC=net"
$ExportPath = ".\Motivosity_$($date).csv"
$ExportXls = ".\Full.xls"
$LogFile = ".\output.log"

# --- FILL THESE IN ---
$hostname = "sftp.motivosity.com"
$port = ""
$user = ""
$pswd = ""

Write-Output "
$(Get-TimeStamp) --- Start of script log. ---" | Out-File $LogFile -append

function Get-TimeStamp {
    
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
    
}

Get-ADUser -Filter {EmployeeID -like "*"} -SearchBase $OUpath -Properties * | Select-Object @{n="First Name";e={$_.givenName}},@{n="Last Name";e={$_.sn}},@{n="Middle Name";e={$_.middleName}},@{n="Email";e={$_.mail}},@{n="Hire Date";e={$_.description}},@{n="Birthday";e={$_.employeeNumber}},@{n="Supervisor Email";e={(get-aduser -property emailaddress $_.manager).emailaddress}},@{n="Title";e={$_.title}},@{n="Department";e={$_.department}},@{n="Country Code";e={"USA"}},@{n="Payroll ID";e={$_.employeeID}},@{n="Action";e={""}} | Export-Csv -Path $ExportPath -NoTypeInformation

# Open the .csv in Excel and save as an .xls, dump output to log.
$xl = new-object -comobject excel.application
$xl.visible = $true
$Workbook = $xl.workbooks.open(“$ExportPath”)
$Workbook.SaveAs($ExportXls,1)
$Workbook.Saved = $True
$xl.Quit()
Write-Output "$(Get-TimeStamp) AD export completed. File located at: $($ExportXls)" | Out-File $LogFile -append


# Load WinSCP .NET assembly
$assemblyPath = if ($env:WINSCP_PATH) { $env:WINSCP_PATH } else { $PSScriptRoot }
Add-Type -Path (Join-Path $assemblyPath "WinSCPnet.dll")

$session = New-Object WinSCP.Session

# Setup session options
$sessionOptions = New-Object WinSCP.SessionOptions -Property @{
    Protocol = [WinSCP.Protocol]::Sftp
    HostName = $hostname
    PortNumber = $port
    UserName = $user
    Password = $pswd
}

$fingerprint = $session.ScanFingerprint($sessionOptions, "SHA-256")
Write-Output "$(Get-TimeStamp) $($fingerprint)" | Out-File $LogFile -append

$newSessionOptions = New-Object WinSCP.SessionOptions -Property @{
    Protocol = [WinSCP.Protocol]::Sftp
    HostName = $hostname
    PortNumber = $port
    UserName = $user
    Password = $pswd
    SshHostKeyFingerprint = $fingerprint
}

try
{
    # Connect
    $session.Open($newSessionOptions)

    # Upload files
    $transferOptions = New-Object WinSCP.TransferOptions
    $transferOptions.TransferMode = [WinSCP.TransferMode]::Binary
 
    $transferResult =
        $session.PutFiles($ExportXls, "/", $False, $transferOptions)
 
     # Throw on any error
    $transferResult.Check()
 
    # Print results
    foreach ($transfer in $transferResult.Transfers)
    {
        Write-Output "$(Get-TimeStamp) Upload of $($transfer.FileName) succeeded" | Out-File $LogFile -append
    }
}
catch
{
    Write-Output "$(Get-TimeStamp) Error: $($_.Exception.Message)" | Out-File $LogFile -append
    Remove-Item -Path $ExportXls
    exit 1
}
finally
{
    # Disconnect, clean up
    $session.Dispose()
}

Remove-Item -Path $ExportXls

Write-Output "$(Get-TimeStamp) --- End of script log. ---
" | Out-File $LogFile -append

Invoke-Item $LogFile
exit 0
