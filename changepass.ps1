# Read the account.txt file
$accounts = Get-Content -Path "account.txt"

# Store the updated account information
$updatedAccounts = @()
$incorrectAccounts = @()

# Iterate through each account
foreach ($account in $accounts) {
    # Split the account details
    $accountDetails = $account -split ","
    $email = $accountDetails[0].Trim()
    $currentPassword = $accountDetails[1].Trim()

    # Check if the email and password are correct
    $isEmailCorrect = $email -eq "correct_email"
    $isPasswordCorrect = $currentPassword -eq "correct_password"

    if ($isEmailCorrect -and $isPasswordCorrect) {
        # Change the password to "password@12PS8s14"
        $newPassword = "password@12PS8s14"

        # Save the updated account information
        $updatedAccount = "$email,$newPassword"
        $updatedAccounts += $updatedAccount

        # Log out the account from all devices (replace this line with your logout logic)
        Write-Host "Logging out account '$email' from all devices..."
    }
    else {
        # Save email and password for incorrect accounts
        $incorrectAccount = "$email,$currentPassword"
        $incorrectAccounts += $incorrectAccount
    }
}

# Save the updated account information to afterchangepass.txt
$updatedAccounts | Out-File -FilePath "afterchangepass.txt"

# Save the email and password for incorrect accounts to baddonne.txt
$incorrectAccounts | Out-File -FilePath "baddonne.txt"

# Display success message
Write-Host "Password change and logout complete."
