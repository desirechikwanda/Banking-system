from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import random as r
import time



class Bank:
	def __init__(self, master):
		self.master = master
		self.master.geometry('600x400+100+50')
		self.master.title('Bank')
		self.master.resizable(False, False)

		#icon = PhotoImage(file='b6.png')
		#self.master.iconphoto(False, icon)

		balance = 0

		con = sqlite3.connect('Bank_Nkhonde.db')
		c = con.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS uers(First_Name text, Surname text, Location text, phone integer, PIN integer,account_number integer, Balance integer); ")
		c.execute("CREATE TABLE IF NOT EXISTS deposits (Amount integer, Account_Number, Period text) ")
		c.execute("CREATE TABLE IF NOT EXISTS withdraws (Amount integer, Account_Number, Period text) ")


		lbl_1 = Label(self.master, text='WELCOME' ,font=('FreeSansBold', 50, 'bold')).place(x=120, y=0)
		lbl_2 = Label(self.master, text=' "Bank Mkhonde" ', font=('FreeSansBold', 15, 'italic')).place(x=210, y=70)

		lbl_3 = Label(self.master, text='Enter Account Number', bg='orange', width=35, font=('FreeSansBold', 20, 'bold')).place(x=0, y=150)
		
		
		acc_nm = StringVar()

		account_nm = Entry(self.master, textvariable = acc_nm, width=35, font=('FreeSansBold', 15, 'bold')).place(x=90, y=190)

		def login():
			
			if acc_nm.get() == '':
				messagebox.showinfo('Error', 'Please Enter Your account Number')
			else:
				c.execute("SELECT * FROM uers WHERE account_number = ? ", (acc_nm.get(),))
				rows = c.fetchall()
				if rows:
					self.master.destroy()
					scrn = Tk()
					scrn.geometry('500x400+100+50')
					scrn.title('Bank')
					scrn.resizable(False, False)

					lbl_9 = Label(scrn,text= 'WELCOME', font=('FreeSansBold', 30, 'bold')).place(x=130, y=0)
					lbl_10 = Label(scrn, text= 'Perform your Transactions Here',bg='orange', width=40, font=('Verdana', 15)).place(x=0, y=45)


					def depo():
						depo  = Toplevel(scrn)
						depo.geometry('400x250+100+50')
						depo.resizable(False, False)
						depo.title('Deposit')

						lbl_11 = Label(depo, text='DEPOSIT', font=('FreeSansBold', 20, 'bold')).place(x=130, y=0)

						lbl_12 = Label(depo, text='Account Number', font=('Verdana', 12)).place(x=20, y=80)
						lbl_13 = Label(depo, text='Amount', font=('Verdana', 12)).place(x=20, y=120)

						global account_namba
						global amount

						account_namba =  StringVar()
						bal = StringVar()
						
						entry_6 = Entry(depo, textvariable = account_namba,width=30, font=('FreeSansBold', 10, 'bold')).place(x=170, y=85)
						entry_7 = Entry(depo, textvariable = bal,width=30, font=('FreeSansBold', 10, 'bold')).place(x=170, y=120)

						
						def submit():
							account = account_namba.get()
							amount = bal.get()

							if account == '' and amount == '':
								messagebox.showinfo('Error', 'Empty Fields')
							elif account  == '':
								messagebox.showinfo('Error', 'Enter Account Number')
							elif amount == '':
								messagebox.showinfo('Error', 'Enter Amount')

							else:
								c.execute("SELECT * FROM uers WHERE account_number = ?", (account,))
								for a,b,p,d,e,f,g in c.fetchall():
									account== f
									

									total = g + int(amount)
									c.execute("UPDATE uers SET Balance =? WHERE account_number = ?", (total, account))
									c.execute("INSERT INTO deposits(Amount , Account_Number, Period ) VALUES (?,?,?) ", (amount, account, time.asctime()))
									con.commit()
									ms = "Depositing of {} MWK is successful and balance is {} MWK ".format(amount, total)	
									messagebox.askokcancel('Info', ms)								
									depo.destroy()		

						btn_5 = Button(depo,bg='royalblue', fg='orange', command = submit, activebackground='grey',cursor='hand2', text = 'SUBMIT', font=('FreeSansBold', 15, 'bold')).place(x=20, y=190)
						btn_6 = Button(depo,bg='royalblue', fg='orange', activebackground='grey', cursor='hand2', text = 'EXIT',command=depo.destroy, font=('FreeSansBold', 15, 'bold')).place(x=280, y=190)
								

					def withdraw():
						bo  = Toplevel(scrn)
						bo.geometry('400x250+100+50')
						bo.resizable(False, False)
						bo.title('withdraw')

						lbl_11 = Label(bo, text='WITHDRAW', font=('FreeSansBold', 20, 'bold')).place(x=130, y=0)

						lbl_12 = Label(bo, text='Account Number', font=('Verdana', 12)).place(x=20, y=80)
						lbl_13 = Label(bo, text='Amount', font=('Verdana', 12)).place(x=20, y=120)

						
						acc_numo = StringVar()
						monie = StringVar()
						entry_6 = Entry(bo, textvariable = acc_numo, width=30, font=('FreeSansBold', 10, 'bold')).place(x=170, y=85)
						entry_7 = Entry(bo, width=30,textvariable=monie, font=('FreeSansBold', 10, 'bold')).place(x=170, y=120)
						
						def draw():
							number = acc_numo.get()
							amount = monie.get()

							if number == '' and amount == '':
								messagebox.showinfo('Error', 'Empty Fields')
							else:
								c.execute("SELECT * FROM uers WHERE account_number = ?", (number,))
								for a,b,p,d,e,f,g in c.fetchall():
									number == f
									
									if g > 0 and g >= int(amount):

										wi = g - int(amount)
									c.execute("UPDATE uers SET Balance =? WHERE account_number = ?", (wi, number))
									c.execute("INSERT INTO withdraws(Amount , Account_Number, Period ) VALUES (?,?,?) ", (amount, number, time.asctime()))
									con.commit()
									ms = "withdraw of {} MWK is successful and balance is {} MWK ".format(amount, wi)	
									messagebox.askokcancel('Info', ms)								
									bo.destroy()		
						

						btn_5 = Button(bo,bg='royalblue', fg='orange', command = draw, activebackground='grey',cursor='hand2', text = 'BORROW', font=('FreeSansBold', 15, 'bold')).place(x=20, y=190)
						btn_6 = Button(bo,bg='royalblue', fg='orange', activebackground='grey', cursor='hand2', text = 'EXIT',command=bo.destroy, font=('FreeSansBold', 15, 'bold')).place(x=280, y=190)

					def enquiry():
						en  = Toplevel(scrn)
						en.geometry('400x250+100+50')
						en.resizable(False, False)
						en.title('Account Inf')

						lbl_11 = Label(en, text='ENQUIRY', font=('FreeSansBold', 20, 'bold')).place(x=130, y=0)

						lbl_12 = Label(en, text='Account Number', font=('Verdana', 12)).place(x=120, y=80)
					
						acc_numa = StringVar()
						entry_6 = Entry(en, textvariable = acc_numa, width=30, font=('FreeSansBold', 10, 'bold')).place(x=90, y=100)
			

						def check():
							if acc_numa.get() == '':
								messagebox.showinfo('Error', 'Enter All Fields')
								
							else:
								c.execute("SELECT * FROM uers WHERE account_number = ?", (acc_numa.get(),))
								for a,b,p,d,e,f,g in c.fetchall():
									acc_numa.get() == f
									info = Tk()
									info.geometry('500x250')
									info.resizable(False, False)
									info.title('Info')

									Full_name = (a, b)
									
									name_label = Label(info, text='Full Name: ' , font=('Verdana', 20, 'bold')).place(x=15, y=40)
									name_label = Label(info, text=' Location: ' , font=('Verdana', 20, 'bold')).place(x=10, y=80)
									name_label = Label(info, text= 'Phone:', font=('Verdana', 20, 'bold')).place(x=15, y=120)
									name_label = Label(info, text= 'Account #:', font=('Verdana', 20,'bold' )).place(x=15, y=165)
									name_label = Label(info, text= 'balance :', font=('Verdana', 20, 'bold')).place(x=15, y=200)
									
									name_label = Label(info, text= Full_name, font=('Verdana', 20)).place(x=200, y=40)
									name_label = Label(info, text= p, font=('Verdana', 20)).place(x=200, y=80)
									name_label = Label(info, text= d, font=('Verdana', 20)).place(x=200, y=120)
									name_label = Label(info, text= f, font=('Verdana', 20)).place(x=200, y=165)
									name_label = Label(info, text= g, font=('Verdana', 20)).place(x=200, y=200)
									name_label = Label(info, text= 'MWK', font=('Verdana', 20, 'bold')).place(x=360, y=200)

									en.destroy()
		
									
						btn_5 = Button(en,bg='royalblue', fg='orange', command = check, activebackground='grey',cursor='hand2', text = 'CHECK', font=('FreeSansBold', 15, 'bold')).place(x=20, y=190)
						btn_6 = Button(en,bg='royalblue', fg='orange', activebackground='grey', cursor='hand2', text = 'EXIT',command=en.destroy, font=('FreeSansBold', 15, 'bold')).place(x=280, y=190)


					def update():
						messagebox.showinfo('Info', 'Option Currently Not Available')
						
					def view():
						view = Tk()
						view.geometry('300x150')
						view.resizable(False, False)
						view.title('Transactions')


						lbl_16 = Label(view, text='Choose Type of  Transactions', font=('Verdana', 10)).place(x=0, y=0)

						
						def deposists():
							view.destroy()
							info = Tk()
							info.geometry('600x400')
							info.resizable(False, False)
							info.title('Deposits')
	

							table =ttk.Treeview(info, columns=['Amount', 'Account_Number', 'Time'], show='headings')
							table.heading('Amount', text='Amount Deposited MWK')
							table.heading('Account_Number', text = 'Account_Number')
							table.heading('Time', text= 'Time')
							table.pack(fill=BOTH, expand=YES)


							c.execute("SELECT * FROM deposits")
							infos = c.fetchall()
							for info in infos:
								table.insert('', END, values=info)
						
						def draws():
							view.destroy()
							info2 = Tk()
							info2.geometry('600x400')
							info2.resizable(False, False)
							info2.title('withdraws')
	

							table =ttk.Treeview(info2, columns=['Amount', 'Account_Number', 'Time'], show='headings')
							table.heading('Amount', text='Amount Withdraw MWK')
							table.heading('Account_Number', text = 'Account_Number')
							table.heading('Time', text= 'Time')
							table.pack(fill=BOTH, expand=YES)


							c.execute("SELECT * FROM withdraws")
							infos = c.fetchall()
							for info in infos:
								table.insert('', END, values=info)



						btn_4 = Button(view, text='DEPOSITS',command=deposists, fg='orange', bg='royalblue', activebackground='grey', cursor = 'hand2', font=('FreeSansBold', 13, 'bold')).place(x=100, y=50)
						btn_4 = Button(view, text='WITHDRAWS',command=draws, cursor='hand2',fg='orange', bg='royalblue',width=20, activebackground='grey', font=('FreeSansBold', 13, 'bold')).place(x=40, y=90)

						
					btn_4 = Button(scrn, text='DEPOSIT',command=depo, fg='orange', bg='royalblue', activebackground='grey', cursor = 'hand2', font=('FreeSansBold', 20, 'bold')).place(x=20, y=90)
					btn_4 = Button(scrn, text='WITHDRAW',command = withdraw, cursor='hand2',fg='orange', bg='royalblue', activebackground='grey', font=('FreeSansBold', 20, 'bold')).place(x=20, y=180)
					btn_4 = Button(scrn, text='UPDATE ',command=update, cursor='hand2',fg='orange', bg='royalblue', activebackground='grey', font=('FreeSansBold', 20, 'bold')).place(x=300, y=90)
					btn_4 = Button(scrn, text='ENQUIRY',command=enquiry, cursor='hand2',fg='orange', bg='royalblue', activebackground='grey', font=('FreeSansBold', 20, 'bold')).place(x=300, y=180)
					btn_4 = Button(scrn, text='VIEW TRANSACTIONS', command=view, cursor='hand2',fg='orange', bg='royalblue', activebackground='grey', font=('FreeSansBold', 15, 'bold')).place(x=110, y=350)
				
				else:
					messagebox.showinfo('Error', 'Invalid Account Number')
		
		btn_1 = Button(self.master,width=20, text='Login', command= login, activebackground='skyblue',cursor = 'hand2', bd='1', relief='raised', font=('FreeSansBold', 15, 'bold')).place(x=155, y=230)
		

		def forgot():
			fgo  = Toplevel(self.master)
			fgo.geometry('400x250+100+50')
			fgo.resizable(False, False)
			fgo.title('Recover Account Number')

			#icon = PhotoImage(file='si.png')
			#fgo.iconphoto(False, icon)

			lbl_14 = Label(fgo, text='Recover your Account Number ', font=('Verdana', 15)).place(x=40, y=5)
			lbl_15 = Label(fgo, text='Please Make sure you Remember you PIN ', font=('Verdana', 8)).place(x=60, y=33)

			lbl_15 = Label(fgo, text='PIN ', font=('Verdana', 30)).place(x=130, y=80)
			
			global pn
			pn = StringVar()
			recover = Entry(fgo,textvariable=pn,width=20,show='*', font=('FreeSansBold', 20, 'bold')).place(x=35, y=130)


			def fogo():
				m = "This option is not available at the moment"
				messagebox.askokcancel('Info', m)

			fog_btn = Button(fgo,command=fogo,  text='SUBMIT', width=20,bg='royalblue', activebackground='skyblue',cursor='hand2', font=('FreeSansBold', 15, 'bold')).place(x=55, y=175)

		btn_1 = Button(self.master,width=20, command = forgot, fg='royalblue', text='Forgot Account Number', activebackground='skyblue',cursor = 'hand2', bd='1', relief='raised', font=('Verdana', 11,)).place(x=180, y=270)
		
		def sign_up():
			new_window = Toplevel(self.master)
			new_window.geometry('500x400+100+50')
			new_window.resizable(False, False)
			new_window.title('sign_up')
			#icon = PhotoImage(file="sign.png")
			#new_window.iconphoto(False, icon)

			lbl_4 = Label(new_window, text='REGISTER', font=('FreeSansBold', 30, 'bold')).place(x=150, y=0)
			lbl_5 = Label(new_window, text='Please make sure you enter all your info', font=('Verdana', 10, )).place(x=130, y=40)

			rd_lbl = Label(new_window, text='Enter Details',width=30, bg='orange', font=('FreeSansBold', 20, 'bold')).place(x=0, y=90)

			lbl_6 = Label(new_window, text='First Name', font=('Verdana', 10 )).place(x=20, y=130)
			lbl_7 = Label(new_window, text='Surname', font=('Verdana', 10)).place(x=20, y=160)
			lbl_8 = Label(new_window, text='Location', font=('Verdana', 10)).place(x=20, y=190)
			lbl_9 = Label(new_window, text='Phone Number', font=('Verdana', 10)).place(x=20, y=220)
			lbl_10 = Label(new_window, text='PIN', font=('Verdana', 10)).place(x=20, y=250)
			

			rfname = StringVar()
			rsname = StringVar()
			rlocation = StringVar()
			rphone = StringVar()
			acc_number = StringVar()
			rpin = StringVar()

			entry_1 = Entry(new_window, textvariable=rfname, width=40,font=('FreeSansBold', 10, 'bold')).place(x=150, y=132)
			entry_2 = Entry(new_window,textvariable = rsname, width=40,font=('FreeSansBold', 10, 'bold')).place(x=150, y=160)
			entry_3 = Entry(new_window,textvariable=rlocation,  width=40,font=('FreeSansBold', 10, 'bold')).place(x=150, y=190)
			entry_4 = Entry(new_window,textvariable = rphone, width=40,font=('FreeSansBold', 10, 'bold')).place(x=150, y=220)
			entry_5 = Entry(new_window,textvariable=rpin,show='*',  width=40,font=('FreeSansBold', 10, 'bold')).place(x=150, y=250)

			btn_3 = Button(new_window, width=5, activebackground='skyblue', relief='raised', bd=1, cursor='hand2',fg='red', text='Quit', command = new_window.destroy, font=('Verdana', 10,'bold')).place(x=20, y=350)
			
			def save():
				acc_number = r.randint(0, 99999999)
				if rfname.get() == '' and rsname.get() == '' and rlocation.get() == '' and rphone.get() == '' and rpin.get() == '':
					messagebox.showinfo('Error', 'Enter All Fields')
				elif rfname.get() == '':
					messagebox.showinfo('Error', 'Enter First Name')
				elif rsname.get() == '':
					messagebox.showinfo('Error', 'Enter provide Surname')
				elif rlocation.get() == '':
					messagebox.showinfo('Error', 'Enter Your location')
				elif rphone.get() == '':
					messagebox.showinfo('Error', 'Provide Phone')
				elif rpin.get() == '':
					messagebox.showinfo('Error', 'Please Provide A PIN')
				else:
					c.execute("SELECT * FROM uers WHERE First_Name = ? AND Surname = ? AND phone = ? AND PIN = ?", (rfname.get(), rsname.get(), rphone.get(), rpin.get()))
					results = c.fetchall()
					if results:
						messagebox.showinfo ('Info', 'User Already Exists')
						
					else:
						c.execute("INSERT INTO uers(First_Name, Surname, Location, Phone, PIN, account_number, Balance) VALUES(?,?,?,?,?,?,?)", (rfname.get() , rsname.get(), rlocation.get() , rphone.get(), rpin.get(), acc_number, balance ))
						con.commit()
						messge = 'You account has been created and your account Number is {} and it has been saved in file'.format(acc_number)
						ok = messagebox.askokcancel('Info', messge)	
						new_file = open('Acount Number', 'w')
						new_file.write(str(acc_number ))
						new_file.close()
						new_window.destroy()		
			
			btn_3 = Button(new_window, width=15,command=save, activebackground='skyblue', relief='raised', bd=1, cursor='hand2',fg='red', text='Save Data', font=('Verdana', 10,'bold')).place(x=200, y=350)
	

		btn_2 = Button(self.master,command=sign_up, text=' Sign Up' ,width=30, fg='green', bd= 2,activebackground='skyblue', cursor='hand2',relief='raised',  font=('FreeSansBold', 15, 'bold')).place(x=100, y=350)


if __name__ == "__main__":
	master = Tk()
	App = Bank(master)
	master.mainloop()