import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime
import winsound

class AlarmClock(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title('Alarm clock')
		self.geometry('900x500')
		self.resizable(0,0)
		self.configure(bg='beige')
		self.widgets = self.get_widgets()

	def get_widgets(self):
		# Setting alarm list widget where we'll store the alarms
		self.alarm_list = self.AlarmList(parent=self, initial_x=760, initial_y=80)
		self.alarm_list.place()

		# Setting frame for clock information with the clock image
		self.clock_frame = tk.Frame(self).pack(expand=True)
		tk.Label(self, text='Alarm Clock by SM', font=('Calibri', 30, 'bold'), bg='beige').place(x=225, y=20)
		self.clock_img = ImageTk.PhotoImage(Image.open('clock.png').resize((700,300)))
		tk.Label(self.clock_frame, image=self.clock_img, bg='beige').place(x=50, y=100)
		
		# Creating labels where the time figures will show
		current_time = self.get_time()
		self.hours_lbl = tk.Label(self.clock_frame, text=current_time[0], font=('ds-digital', 150), bg='beige')
		self.minutes_lbl = tk.Label(self.clock_frame, text=current_time[1], font=('ds-digital', 150), bg='beige')
		self.seconds_lbl = tk.Label(self.clock_frame, text=current_time[2], font=('ds-digital', 50), bg='beige')
		
		self.hours_lbl.place(x=80, y=150)
		self.minutes_lbl.place(x=400, y=150)
		self.seconds_lbl.place(x=650, y=270)


		# Validation method to allow only integers
		self.vcmd = (self.register(self.validate),
				'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

		# Creating the alarm-setting menu
		self.alarm_set_lbl = tk.Label(text='Set Alarm Clock', font=('Calibri', 15, 'bold'), bg='beige')
		self.hour_input = tk.Entry(self.clock_frame, name='hour_input', validate='key', validatecommand=self.vcmd, width=5)
		self.minute_input = tk.Entry(self.clock_frame, name='minute_input', validate='key', validatecommand=self.vcmd, width=5)
		self.second_input = tk.Entry(self.clock_frame, name='second_input', validate='key', validatecommand=self.vcmd, width=5)
		self.start_btn = tk.Button(self.clock_frame,text='Set  Alarm', bg='green', fg='white', font=('Calibri', 12, 'bold'), border=5, highlightcolor='gray', command=lambda self=self: self.create_alarm())
		self.stop_btn = tk.Button(self.clock_frame,text='Stop Alarm', bg='red', fg='white', font=('Calibri', 12, 'bold'), border=5, highlightcolor='gray', command=lambda self=self: self.alarm_off())

		self.alarm_set_lbl.place(x=80, y=420)
		self.hour_input.place(x=80, y=460)
		self.minute_input.place(x=120, y=460)
		self.second_input.place(x=160, y=460)
		self.start_btn.place(x=220, y=450)
		self.stop_btn.place(x=340, y=450)
		
		self.alarm_off()

	# Function to get the current time in "hh:mm:ss" format
	def get_time(self):
		now = datetime.now()
		return ("{:02d}".format(now.hour), "{:02d}".format(now.minute), "{:02d}".format(now.second))
	
	# Function to keep the clock running and stop any possible alarm
	def alarm_off(self):
		winsound.PlaySound(None, winsound.SND_PURGE)
		current_time = self.get_time()
		
		self.hours_lbl.configure(text=current_time[0])
		self.minutes_lbl.configure(text=current_time[1])
		self.seconds_lbl.configure(text=current_time[2])

		is_alarm_on = self.check_alarms(current_time=current_time)

		if not is_alarm_on:
			self._job = self.after(1000, self.alarm_off)

	# Function to stop clock running and play sound in a loop
	def alarm_on(self):
		if self._job is not None:
			self.after_cancel(self._job)
			self._job = self.after(1000, lambda: winsound.PlaySound('alarm.wav', winsound.SND_LOOP + winsound.SND_ASYNC))
	
	# Function to validate time entries with possible time selections(hours from 0 to 24 and minutes/seconds from 0 to 60).
	def validate(self, action, index, value_if_allowed,
					   prior_value, text, validation_type, trigger_type, widget_name):
		if action != '1':
			return True

		if action == '1' and value_if_allowed:
			try:
				if len(value_if_allowed) > 3:
					return False
					
				if widget_name == '.hour_input' and float(value_if_allowed) >= 0 and float(value_if_allowed) <= 24:
					return True
				elif (widget_name == '.minute_input' or widget_name == '.second_input') and float(value_if_allowed) >= 0 and float(value_if_allowed) <= 60:
					return True
				else:
					return False
			except ValueError:
				return False
		else:
			return False
	
	# Function to get time figures from entries and add them into the alarm list
	def create_alarm(self):
		hour = "{:02d}".format(int(self.hour_input.get())) if self.hour_input.get() != '' else "00"
		minute = "{:02d}".format(int(self.minute_input.get())) if self.minute_input.get() != '' else "00"
		second = "{:02d}".format(int(self.second_input.get())) if self.second_input.get() != '' else "00"

		self.alarm_list.add_alarm(text=hour+':'+minute+':'+second)

	# Function to check if the current_time is within the alarm list, so it can activate the alarm
	def check_alarms(self, current_time):
		current_time = current_time[0]+":"+current_time[1]+":"+current_time[2]
		alarms = self.alarm_list.alarm_list
		
		for alarm in alarms:
			if alarm == current_time:
				self.alarm_on()
				return True
		
		return False

	class AlarmList(tk.Frame):
		def __init__(self, parent,initial_x, initial_y):
			tk.Frame.__init__(self, parent, height=500, width=200, bg='beige')
			self.place(x=initial_x,y=initial_y)
			self.gap = 30
			self.x = 10
			self.y = 30
			self.next_y = self.y + self.gap
			self.alarm_list = []
			tk.Label(self, text='Alarm List', font=('Calibri', 15, 'bold'), bg='beige').place(x=self.x, y=self.y, bordermode='outside')
	
		def add_alarm(self, text):
			self.get_alarm_list()
			if text in self.alarm_list:
				return

			self.y += self.gap
			tk.Label(self, text=text, bg='beige').place(x=self.x, y=self.y)
			self.get_alarm_list()
		
		def get_alarm_list(self):
			self.alarm_list = []
			for label in self.winfo_children():
				if label.widgetName == 'label':
					self.alarm_list.append(label.cget('text'))

			return self.alarm_list

clock = AlarmClock()
clock.mainloop()
