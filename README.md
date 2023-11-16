# Error entrypoint
The error you're encountering is due to the presence of Windows-style carriage return (CR) characters ('\r') in the entrypoint.sh file. These CR characters are not recognized by the Bash shell on Linux and are being interpreted as commands, causing the errors you're seeing.

To resolve this issue, you need to replace the Windows-style CR characters with Unix-style line feed (LF) characters ('\n'). You can do this using a text editor that supports converting file formats. For example, in Notepad++, you can use the Edit > EOL Conversion > UNIX (LF) option.