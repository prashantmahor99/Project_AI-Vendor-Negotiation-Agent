import pythoncom
import win32com.client

pythoncom.CoInitialize()

try:
    outlook = win32com.client.gencache.EnsureDispatch("Outlook.Application")

    namespace = outlook.GetNamespace("MAPI")

    inbox = namespace.GetDefaultFolder(6)

    print("Connected Successfully")
    print("Inbox:", inbox.Name)

finally:
    pythoncom.CoUninitialize()

messages = inbox.Items

print("Total mails:", messages.Count)

for i in range(1, min(messages.Count, 6)):
    msg = messages.Item(i)
    print("-------------------")
    print(msg.Subject)
    print("Unread:", msg.UnRead)
    print("Attachments:", msg.Attachments.Count)      