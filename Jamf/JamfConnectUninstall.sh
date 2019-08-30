#!/bin/bash
#
#Remove Jamf Connect Login and Jamf Connect Sync
#
#V1.0
#     Allen Armas 2019.08.27
#

logfile="/Library/Logs/JamfConnectUninstall"

#Jamf Connect Login Verification and removal

if [[ -e "/usr/local/bin/authchanger" ]]; then
	#Verify Jamf Connect Login Version
	JCLoginVersion=`/usr/local/bin/authchanger -version`
	/bin/echo "`date`: Current Jamf Connect version: ${JCLoginVersion}" >> ${logfile}

	#Reset Mac OS authentication database to factory settings
	/bin/echo "`date`: Resetting the authentication database to macOS factory settings" >> ${logfile}
	/usr/local/bin/authchanger -reset
	/bin/echo "`date`: Successfully Reset the authentication database to macOS factory settings" >> ${logfile}
	/bin/sleep 5

	#Remove Jamf Connect Login
	/bin/echo "`date`: Removing Jamf Connect Login" >> ${logfile}
	/bin/rm /usr/local/bin/authchanger
	/bin/rm /usr/local/lib/pam/pam_saml.so.2
	/bin/rm -rf /Library/Security/SecurityAgentPlugins/JamfConnectLogin.bundle
	/bin/echo "`date`: Successfully Removed Jamf Connect Login" >> ${logfile}
	/bin/sleep 5
else
	/bin/echo "`date`: Jamf Connect Login not installed. Exiting" >> ${logfile}
fi

#Jamf Connect Sync Verification and Removal

if [[ -e "/Applications/Jamf Connect Sync.app" ]]; then
	JCSyncVersion=`/usr/bin/defaults read '/Applications/Jamf Connect Sync.app/Contents/Info' CFBundleShortVersionString`
	#Verify Jamf Connect SyncVersion
	/bin/echo "`date`: Current Version of Jamf Connect Sync: ${JCSyncVersion}" >> ${logfile}
	/bin/sleep 5

	#Remove Jamf Connect Sync
	/bin/rm -rf '/Applications/Jamf Connect Sync.app'
	/bin/echo "`date`: Successfully Removed Jamf Connect Sync" >> ${logfile}

	#Remove Jamf Connect Sync Launch Agent
	/bin/rm -rf '/Library/LaunchAgents/com.jamf.connect.sync.plist'
	/bin/echo "`date`: Successfully Removed Jamf Connect Sync Launch Agent" >> ${logfile}

	#Kill Jamf Connect Sync Application
	pkill "Jamf Connect Sync"
	/bin/echo "`date`: Killing Application: Jamf Connect Sync" >> ${logfile}
	/bin/sleep 5
	exit 0
else
	/bin/echo "`date`: Jamf Connect Sync not installed. Exiting" >> ${logfile}
	exit 1
fi
