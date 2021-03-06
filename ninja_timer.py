from tkinter import Tk, Label, StringVar, Button, Frame, Entry, Text, INSERT
from tkinter.messagebox import askquestion, showwarning

DEFAULT_TIME_COUNT = 3600

class MyRoot(Tk):
	def __init__(self, master=None):
		Tk.__init__(self, master)
		self.last_time_count = DEFAULT_TIME_COUNT

		self.hour_str = StringVar()
		self.minute_str = StringVar()
		self.second_str = StringVar()
		self.time_str = StringVar()
		self.status_str = StringVar()
		self.edit_str = StringVar()
		self.time_str.set('60:00')
		self.status_str.set('开始')
		self.edit_str.set('保存')

		self.timer_frame = Frame(self)
		self.timer_frame.pack(side='top', fill='both')

		self.input_hour = Entry(self.timer_frame, width=3, textvariable=self.hour_str)
		self.input_hour.pack(side='left', fill='both')
		self.input_hour.insert(INSERT, "1")

		self.sign_one = Label(self.timer_frame, text=':', width=1)
		self.sign_one.pack(side='left', fill='both')

		self.input_minute = Entry(self.timer_frame, width=3, textvariable=self.minute_str)
		self.input_minute.pack(side='left', fill='both')
		self.input_minute.insert(INSERT, "00")

		self.sign_two = Label(self.timer_frame, text=':', width=1)
		self.sign_two.pack(side='left', fill='both')
		

		self.input_second = Entry(self.timer_frame, width=3, textvariable=self.second_str)
		self.input_second.pack(side='left', fill='both')
		self.input_second.insert(INSERT, "00")


		self.label = Label(self, textvariable=self.time_str, width=10)
		self.label.pack(side='top', fill='both')

		self.start_button = Button(self, textvariable=self.status_str, command=self.toggle, state='disabled')
		self.start_button.pack(side='top', fill='both')

		self.edit_button = Button(self, textvariable=self.edit_str, command=self.edit)
		self.edit_button.pack(side='top', fill='both')

		self.time_count = DEFAULT_TIME_COUNT
		self.current_status = False  # False 代表 暂停  True 代表 播放
		self.edit_status = False		
		self.is_first = False

		self.show_edit()

	def toggle(self):
		self.current_status = not self.current_status
		if self.current_status:
			self.play()
		else:
			self.pause()

	def play(self):
		if self.time_count == 0:									
			showwarning('请注意！', '起来喝水了！！ 回来以后!')
			self.reset()			
			return	
		
		self.status_str.set('暂停')		
		self.run_time()
		self.timer = self.after(1000, self.play)

	def pause(self):
		self.status_str.set('运行')
		self.after_cancel(self.timer)		

	def reset(self):
		self.time_count = self.last_time_count
		self.current_status = False
		self.run_time()		
		self.pause()	
	
	def set_label_time(self):
		time_format_dict = self.format_time()
		hour = time_format_dict['hour']
		minute = time_format_dict['minute']
		second = time_format_dict['second']		
		self.time_str.set('%d:%02d:%02d' % (hour, minute, second))

	def run_time(self):
		self.set_label_time()		
		self.time_count -= 1

	def format_time(self):
		hour = self.time_count // 3600
		hour_mod = self.time_count % 3600
		minute = hour_mod // 60
		minute_mod = hour_mod % 60
		second = minute_mod % 60
		return {'hour': hour, 'minute': minute, 'second': second}


	def set_time(self, time_dict):
		self.time_count = time_dict['hour'] * 3600 + time_dict['minute'] * 60 + time_dict['second'];
		self.last_time_count = self.time_count

	def get_time(self):
		hour_text = self.input_hour.get()
		minute_text = self.input_minute.get()
		second_text = self.input_second.get()

		time_dict = {}
		time_dict['hour'] = int(hour_text)
		time_dict['minute'] = int(minute_text)
		time_dict['second'] = int(second_text)

		return time_dict

	def validate_time(self):
		result_dict = self.validate_hour()
		if not result_dict['accept']:
			showwarning('warning', result_dict['msg'])
			return False

		result_dict = self.validate_minute()
		if not result_dict['accept']:
			showwarning('warning', result_dict['msg'])
			return False

		result_dict = self.validate_second()
		if not result_dict['accept']:
			showwarning('warning', result_dict['msg'])
			return False

		return True

	def validate_hour(self):
		hour_str = self.input_hour.get()
		result_dict = {'accept': True, 'msg': None}
		if not hour_str.isdigit():
			result_dict['accept'] = False
			result_dict['msg'] = '小时数不为整数'
			return result_dict

		return result_dict

	def validate_minute(self):
		minute_str = self.input_minute.get()
		result_dict = {'accept': True, 'msg': None}
		if not minute_str.isdigit():
			result_dict['accept'] = False
			result_dict['msg'] = '分钟数不为整数'
			return result_dict

		minute_num = int(minute_str)
		if minute_num >= 60:
			result_dict['accept'] = False
			result_dict['msg'] = '分钟数不能大于等于60'
			return result_dict

		return result_dict

	def validate_second(self):
		second_str = self.input_second.get()
		result_dict = {'accept': True, 'msg': None}
		if not second_str.isdigit():
			result_dict['accept'] = False
			result_dict['msg'] = '秒数不为整数'
			return result_dict

		second_num = int(second_str)
		if second_num >= 60:
			result_dict['accept'] = False
			result_dict['msg'] = '秒数不能大于60'
			return result_dict

		return result_dict

	def edit(self):
		self.toggle_edit()
	

	def toggle_edit(self):
		if self.edit_status:
			self.switch_to_edit()
		else:
			self.completed_edit()

		self.edit_status = not self.edit_status

	def switch_to_edit(self):
		self.show_edit()
		self.start_button.config({'state': 'disabled'});
		self.force_pause()
		self.edit_str.set('保存')
		self.set_current_time_to_input()

	def force_pause(self):
		if self.current_status:
			self.toggle()	

	def set_current_time_to_input(self):
		time_format_dict = self.format_time()
		hour = time_format_dict['hour']
		minute = time_format_dict['minute']
		second = time_format_dict['second']
		self.hour_str.set(hour)
		self.minute_str.set(minute)		
		self.second_str.set(second)

	def completed_edit(self):
		if self.validate_time():
			self.set_time(self.get_time())
			self.edit_str.set('编辑')
			self.set_label_time()
			self.hide_edit()
			self.start_button.config({'state': 'normal'})
		else:
			self.edit_status = not self.edit_status

	def hide_edit(self):
		self.timer_frame.pack_forget()
		self.label.pack(side='top', fill='both', before=self.start_button)		
		

	def show_edit(self):
		self.timer_frame.pack(side='top', fill='both', before=self.start_button)
		self.label.pack_forget()		


def close_window():	
	root.destroy()	

if __name__ == '__main__':
	# root = Tk()
	root = MyRoot()
	# my_frame.pack(side='top', fill='both')
	root.title('起来喝水！')
	root.protocol('WM_DELETE_WINDOW', close_window)
	root.mainloop()
	


