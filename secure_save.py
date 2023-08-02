import tkinter as tk
import subprocess

# create the main window
root = tk.Tk()
root.title("Wi-Fi Passwords")

# create a label
label = tk.Label(root, text="Wi-Fi Passwords", font=("Helvetica", 20, "bold"))
label.pack(pady=10)

# create a text box to display the passwords
text = tk.Text(root, width=50, height=20)
text.pack(padx=10, pady=10)

# function to retrieve the Wi-Fi profiles and passwords
def get_passwords():
    # clear any existing text in the text box
    text.delete('1.0', tk.END)

    # get the list of Wi-Fi profiles
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
    data = meta_data.decode('utf-8', errors='backslashreplace')
    data = data.split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

    # retrieve the passwords for each profile
    for profile in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
            results = results.decode('utf-8', errors='backslashreplace')
            results = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]

            # add the profile name and password to the text box
            text.insert(tk.END, f"{profile}: {results[0]}\n")
        except subprocess.CalledProcessError:
            text.insert(tk.END, f"{profile}: Encoding Error Occurred\n")

# create a button to retrieve the passwords
button = tk.Button(root, text="Get Passwords", command=get_passwords)
button.pack(pady=10)

# start the main loop
root.mainloop()