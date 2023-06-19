import tkinter as tk
from tkinter import messagebox
from Snapp import SnappTaxi
from errors.http_error import VoucherExceededException, PhoneInvalidException


MY_NUMBER = '0919*******'
        
class LoginFrame(tk.Frame):
    def __init__(self, master=None, switch_frame_callback=None, snapp=None):
        
        super().__init__(master)
        self.master = master
        self.snapp = snapp
        self.switch_frame_callback = switch_frame_callback
        self.grid()
        

        self.phone_label = tk.Label(self, text="Your phone number")
        self.phone_label.grid(row=0, column=0)

        self.phone_entry = tk.Entry(self, )
        self.phone_entry.insert(0, MY_NUMBER)  # Add placeholder text
        self.phone_entry.bind("<FocusIn>", self.clear_placeholder)  # Clear placeholder text when the user clicks on the Entry
        self.phone_entry.grid(row=0, column=1)


        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send Sms Code"
        
        # Handle send sms code
        #snapp_instance = SnappTaxi()
        self.send_button["command"] = self.send_code
        self.send_button.grid(row=1, column=0)

        self.code_label = tk.Label(self, text="Code")
        self.code_label.grid(row=2, column=0)

        self.code_entry = tk.Entry(self)
        self.code_entry.grid(row=2, column=1)

        self.verify_button = tk.Button(self)
        self.verify_button["text"] = "Accept Code"
        self.verify_button["command"] = self.verify_code
        self.verify_button.grid(row=3, column=0)



    def clear_placeholder(self, event):
        if self.phone_entry.get() == MY_NUMBER:
            self.phone_entry.delete(0, tk.END)


    def send_code(self):

        if self.phone_entry.get() != MY_NUMBER :

            self.snapp.update_user_number(self.phone_entry.get())
    
            try:
                token = self.snapp.load_token()
        
                if token:
                    messagebox.showinfo("Success", "Your logged in !")
                    self.switch_frame_callback()
                else:
                    
                    self.snapp.send_sms()
                    self.send_button.destroy()
                    messagebox.showinfo("Info", "Token not found! The verification code has been sent to your phone number.")

            except PhoneInvalidException as e:
                messagebox.showinfo("error", str(e))
            
            except Exception as e:
                raise(e)
                

    def verify_code(self):
    
        if self.code_entry.get() and self.phone_entry.get():

            # Run the async function in the event loop
            result = self.snapp.login(self.code_entry.get())
            
            if result:
                messagebox.showinfo("Success", "Your logged in !")
                self.switch_frame_callback()
            else:
                messagebox.showinfo("Error", "Error !")


class MainApplicationFrame(tk.Frame):
    def __init__(self, master=None, snapp:SnappTaxi=None):
        super().__init__(master)
        self.master = master
        self.snapp = snapp
        self.grid()

        
        self.prize_text_label = tk.Label(self, text="prize text:")
        self.prize_text_label.grid(row=1, column=0)
        self.prize_text_entry = tk.Entry(self)
        self.prize_text_entry.grid(row=1, column=1)


        self.count_label = tk.Label(self, text="Voucher Count:")
        self.count_label.grid(row=2, column=0)
        self.count_entry = tk.Entry(self)
        self.count_entry.grid(row=2, column=1)


        self.send_button = tk.Button(self)
        self.send_button["text"] = "redeem"
        self.send_button["command"] = self.reedem_prize
        self.send_button.grid(row=3, column=1)

        # self.counter_label = tk.Label(self, text='')
        # self.counter_label.grid(row=4, column=1)

        self.counter_label = tk.Label(self, text='None')
        self.counter_label.grid(row=5, column=1)

    def reedem_prize(self):
        
        self.snapp.load_token()
        prize_id = self.snapp.get_reward_id_by_name(self.prize_text_entry.get())
        

        if prize_id :

            for i in range(1, int(self.count_entry.get()) + 1):
                
                try:
                    self.counter_label.config(text=f'{i} Voucher redeemed successfully')
                    self.update_idletasks()  # Force update the GUI
                    self.snapp.redeem_prize(prize_id)
                    # self.master.after(2000, lambda: self.master.focufos_force())  # Bring focus back to the root window after 2 seconds
                
                except VoucherExceededException as e:
                    messagebox.showinfo("ERROR", str(e))
                    break
                    
                except RuntimeError as e:
                    messagebox.showinfo("ERROR", "Error !")
                    break

            else:
                messagebox.showinfo("Successful", "All coupons have been successfully received")
        else:
            messagebox.showinfo("ERROR", "prize not found !")

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.snapp = SnappTaxi()
        self.geometry("300x300")
        self.login_frame = LoginFrame(self, self.show_main_frame, self.snapp)
        self.main_frame = MainApplicationFrame(self, self.snapp)
        self.show_login_frame()

    def show_login_frame(self):
        self.main_frame.grid_remove()
        self.login_frame.grid()

    def show_main_frame(self):
        self.login_frame.grid_remove()
        self.main_frame.grid()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
