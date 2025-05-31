# In-memory storage (not persistent! Data will be lost when the program closes)
users = {}  # Stores: {username: password}
emails = [] # Stores: [{"sender": "user1", "recipient": "user2", "subject": "Hi", "body": "Hello there!"}]
chat_messages = [] # Stores: [{"sender": "user1", "message": "Hey everyone!"}]

current_user = None # To keep track of the currently logged-in user

def register():
    """Handles new user registration."""
    while True:
        username = input("Enter a new username: ").strip()
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
        if username in users:
            print("Username already taken. Please choose another.")
        else:
            password = input("Enter a password: ").strip()
            if not password:
                print("Password cannot be empty. Please try again.")
                continue
            users[username] = password
            print(f"User '{username}' registered successfully!")
            break

def login():
    """Handles user login."""
    global current_user # Allows modification of the global current_user variable
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if username in users and users[username] == password:
            current_user = username
            print(f"Welcome, {username}!")
            return True # Login successful
        else:
            print("Invalid username or password. Please try again.")
            return False # Login failed

def logout():
    """Logs out the current user."""
    global current_user
    if current_user:
        print(f"Goodbye, {current_user}!")
        current_user = None
    else:
        print("No user is currently logged in.")

def compose_email():
    """Allows the current user to send an internal email."""
    if not current_user:
        print("Please log in to send emails.")
        return

    while True:
        recipient = input("Enter recipient username: ").strip()
        if recipient not in users:
            print("Recipient does not exist. Please enter a valid username.")
        elif recipient == current_user:
            print("You cannot send an email to yourself.")
        else:
            break

    subject = input("Enter email subject: ").strip()
    print("Enter email body (type 'END' on a new line by itself to finish):")
    email_body_lines = []
    while True:
        line = input() # Read a line of input
        if line.strip().upper() == 'END': # CHECK HERE: Check if the stripped, upper-cased line is 'END'
            break # If it is, break out of the loop
        email_body_lines.append(line) # Otherwise, add the line to the list
    full_body = "\n".join(email_body_lines) # Join all collected lines

    emails.append({
        "sender": current_user,
        "recipient": recipient,
        "subject": subject,
        "body": full_body
    })
    print("Email sent successfully!")

def view_inbox():
    """Displays emails received by the current user."""
    if not current_user:
        print("Please log in to view your inbox.")
        return

    user_inbox = [email for email in emails if email["recipient"] == current_user]

    if not user_inbox:
        print("Your inbox is empty.")
        return

    print("\n--- Your Inbox ---")
    for i, email in enumerate(user_inbox):
        print(f"--- Email {i+1} ---")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Body:\n{email['body']}")
        print("-------------------")
    print("--------------------\n")

def view_sent_emails():
    """Displays emails sent by the current user."""
    if not current_user:
        print("Please log in to view your sent emails.")
        return

    user_sent = [email for email in emails if email["sender"] == current_user]

    if not user_sent:
        print("You haven't sent any emails.")
        return

    print("\n--- Your Sent Emails ---")
    for i, email in enumerate(user_sent):
        print(f"--- Sent Email {i+1} ---")
        print(f"To: {email['recipient']}")
        print(f"Subject: {email['subject']}")
        print(f"Body:\n{email['body']}")
        print("-------------------")
    print("------------------------\n")

def send_chat_message():
    """Allows the current user to send a message to the public chat."""
    if not current_user:
        print("Please log in to chat.")
        return

    message = input("Enter your chat message: ").strip()
    if message:
        chat_messages.append({"sender": current_user, "message": message})
        print("Message sent to chat.")
    else:
        print("Message cannot be empty.")

def view_chat_history():
    """Displays the history of all chat messages."""
    if not current_user:
        print("Please log in to view chat history.")
        return

    if not chat_messages:
        print("No chat messages yet.")
        return

    print("\n--- Chat History ---")
    for msg in chat_messages:
        print(f"[{msg['sender']}]: {msg['message']}")
    print("--------------------\n")

def show_menu():
    """Displays the appropriate menu based on login status."""
    print("\n--- Main Menu ---")
    if current_user:
        print(f"Logged in as: {current_user}")
        print("1. Compose Email")
        print("2. View Inbox")
        print("3. View Sent Emails")
        print("4. Send Chat Message")
        print("5. View Chat History")
        print("6. Logout")
    else:
        print("1. Register")
        print("2. Login")
    print("0. Exit")
    print("-----------------")

def main():
    """The main application loop."""
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if current_user: # Menu options for logged-in users
            if choice == '1':
                compose_email()
            elif choice == '2':
                view_inbox()
            elif choice == '3':
                view_sent_emails()
            elif choice == '4':
                send_chat_message()
            elif choice == '5':
                view_chat_history()
            elif choice == '6':
                logout()
            elif choice == '0':
                print("Exiting application. All data will be lost.")
                break
            else:
                print("Invalid choice. Please try again.")
        else: # Menu options for logged-out users (Register/Login)
            if choice == '1':
                register() # Call the register function
            elif choice == '2':
                login() # Call the login function
            elif choice == '0':
                print("Exiting application. All data will be lost.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
