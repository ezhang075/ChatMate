# Edward Zhang
# junz23@uci.edu
# 42058839


import tkinter as tk
from tkinter import ttk, simpledialog
import ds_messenger
import Profile
from pathlib import Path
import json
# 168.235.86.101


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send",
                                width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, dsuserver=None):
        self.root = root
        self.dsuserver = dsuserver
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.dsuserver)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.dsuserver = self.server_entry.get()


class SigninDialog(simpledialog.Dialog):
    def __init__(self, root):
        self.root = root
        self.username = ""
        self.password = ""
        self.dsuserver = ""
        super().__init__(root, "Sign into Profile")

    def body(self, frame):
        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.username)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.password)
        self.password_entry.pack()

    def apply(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()


class CreateAccountDialog(simpledialog.Dialog):
    def __init__(self, root):
        self.root = root
        self.username = ""
        self.password = ""
        self.dsuserver = ""
        super().__init__(root, "Create an Account")

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.dsuserver)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.username)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.password)
        self.password_entry.pack()

    def apply(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.dsuserver = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.dsuserver = None
        self.recipient = None
        self.message = None
        self.profile = None
        self.direct_messenger = None

        self._draw()
        self.check_new()

    def send_message(self):
        self.message = self.body.get_text_entry()
        print(self.message)
        token = self.direct_messenger._token
        print(token)

    def load_friends(self):
        try:
            with open(f'{self.username}.dsu', 'r') as file:
                json_data = file.read()
                data = json.loads(json_data)
                friends = data.get('friends', [])
                for friend in friends:
                    self.body.insert_contact(friend)
        except FileNotFoundError:
            print("Profile file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

    def add_contact(self):
        new_contact_username = tk.simpledialog.askstring(
            "Add Contact",
            "Enter the username of your friend:")

        if new_contact_username:
            self.body.insert_contact(new_contact_username)
            profile = Profile.Profile()
            profile.load_profile(f'{self.username}.dsu')
            profile.add_friend(new_contact_username)
            profile.save_profile(f'{self.username}.dsu')

    def sign_in_profile(self):
        dialog = SigninDialog(self.root)
        self.username = dialog.username
        self.password = dialog.password

        if self.authenticate_user(self.username, self.password):
            print("Successfully signed in!")
        else:
            print("Failed to sign in! Please try again!")

        self.dsuserver = self.profile.dsuserver

        if (self.username is not None and
                self.password is not None and
                self.dsuserver is not None):
            self.direct_messenger = ds_messenger.DirectMessenger(
                dsuserver=self.dsuserver,
                username=self.username,
                password=self.password)

    def create_account_profile(self):
        dialog = CreateAccountDialog(self.root)
        self.username = dialog.username
        self.password = dialog.password
        self.dsuserver = dialog.dsuserver
        print('server;', self.dsuserver)

        try:
            self.create_file(self.username)
            self.create_new_profile(
                self.username,
                self.password,
                self.dsuserver)
            print("Successfully created an account!")
            self.check_new

        except:
            print("Failed to create an account. Please try again.")

        if (self.username is not None and
                self.password is not None and
                self.dsuserver is not None):
            self.direct_messenger = ds_messenger.DirectMessenger(
                dsuserver=self.dsuserver,
                username=self.username,
                password=self.password)

    def create_file(self, username):
        if Path(f'{username}.dsu').touch():
            return True
        else:
            return False

    def create_new_profile(self, username, password, server):
        try:
            profile = Profile.Profile(server, username, password)
            profile.save_profile(f'{username}.dsu')
            return True
        except:
            return False

    def authenticate_user(self, username, password):
        profile = Profile.Profile()

        try:
            profile.load_profile(f'{username}.dsu')
            for friend in profile.friends:
                self.body.insert_contact(friend)

            if profile.username == username and profile.password == password:
                self.profile = profile
                return True
            else:
                return False

        except:
            return False

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.display_friend_messages(recipient)

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.dsuserver)
        self.username = ud.user
        self.password = ud.pwd
        self.dsuserver = ud.dsuserver

    def publish(self):
        self.message = self.body.get_text_entry()
        print(self.message)
        if self.direct_messenger is not None:
            try:
                send = self.direct_messenger.send(self.message, self.recipient)

                if send is True:
                    my_message = ds_messenger.DirectMessage(recipient=self.recipient, message=self.message)
                    profile = Profile.Profile()
                    profile.load_profile(f'{self.username}.dsu')
                    profile.add_message(my_message)
                    profile.save_profile(f'{self.username}.dsu')
                    self.body.insert_user_message(self.message)
                    self.body.set_text_entry("")

            except:
                print('Cannot send')

    def check_new(self):
        if self.profile is not None:
            new_messages, message_string = self.direct_messenger.retrieve_new()
            print('NEW MESSAGE:', new_messages)

            if new_messages:
                for message in new_messages:
                    self.profile.add_message(message)
                    if message.recipient == self.recipient:
                        if message.recipient != self.profile.username:
                            self.body.insert_contact_message(message._message)
                    else:
                        self.body.insert_user_message(message._message)

                self.profile.save_profile(f'{self.username}.dsu')

        self.root.after(1000, self.check_new)

    def display_friend_messages(self, friend):
        if self.profile is not None:
            self.body.entry_editor.delete('1.0', tk.END)
            for message in self.profile.get_friend_messages(friend):
                if message._timestamp == 0:
                    self.body.insert_user_message(message._message)
                else:
                    self.body.insert_contact_message(message._message)

    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(
            label='Add Contact',
            command=self.add_contact)
        settings_file.add_command(
            label='Sign into Profile',
            command=self.sign_in_profile)
        settings_file.add_command(
            label='Create an Account',
            command=self.create_account_profile)
        self.body = Body(
            self.root,
            recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.publish)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
