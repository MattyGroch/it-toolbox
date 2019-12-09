New-PSSession -ComputerName ssdc03.snapsheet.net
Import-Module -PSsession $S -Name ActiveDirectory
function AuditAttribute {
    param($Filter)
    $OU = "OU=Users,OU=Internal,DC=snapsheet,DC=net"
    $count = 0
    $key = @{
        PayrollID = '(EmployeeID -notlike "*") -And (company -eq "Snapsheet")';
        Birthday = '(EmployeeNumber -notlike "*") -And (company -eq "Snapsheet")';
        HireDate = '(Description -notlike "*") -And (company -eq "Snapsheet")'
        }


    $users = Get-ADUser -Filter $key.$Filter -SearchBase $OU -Properties * | Select displayname,sAMAccountName
    $output = ''
    
    Foreach ($user in $users){
        $output += "-- " + $user.displayname + " (" + $user.sAMAccountName + ")"
        $output += "`n"
        $count = $count + 1
        }

    If ($count -eq 0) {
        $result = "No" + $Filter + "errors found."
        return $result
    } Else {
        $result = "_Total Errors: " + $count + "_`n" + $output
        return $result
    }
}

$payroll = AuditAttribute -Filter PayrollID
$birthday = AuditAttribute -Filter Birthday
$hiredate = AuditAttribute -Filter HireDate

$webhook = 'https://hooks.zapier.com/hooks/catch/4450428/o44cl1o/'

$Body = @{ payroll=$payroll; birthday=$birthday; hiredate=$hiredate }

$params = @{
    Headers = @{'accept'='application/json'}
    Body = ($Body | convertto-json)
    Method = 'Post'
    URI = $webhook 
}

# Invoke-RestMethod @params