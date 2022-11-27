import threading
import time
from tkinter import *
from customtkinter import *
import customtkinter


customtkinter.set_appearance_mode("system")
class StopWatch(CTk, Tk):
    destroy_start_btn = False
    destroy_stop_btn = False
    add_frame = True
    lab_array = []
    lab_increment = 1
    started = False
    running = False
    passed = 0
    previous_passed = 0
    lab = 1
    # def __int__(self):
    #     super(StopWatch, self).__int__()

    def on_start(self):
        self.time_label= customtkinter.CTkLabel(master=self, text=f'00:00:00:00', text_color='white', text_font=(None, 25),)
        self.time_label.place(relwidth= .8, relheight= .122, relx= .1, rely= .1)

        self.start_btn = customtkinter.CTkButton(master=self, text='start'.upper(), text_color='white',
                                                 text_font=(None, 20), hover_color='black',command=self.start)
        self.start_btn.place(relwidth=.8, relheight=.122, relx=.1, rely=.8)

    def start(self):
        self.start_btn.configure(text='stop'.upper(), command=self.stop_resume)
        self.lab_btn = customtkinter.CTkButton(master=self, text='lab'.upper(),
                                                text_color='white',
                                                text_font=(None, 20), hover_color='black', command=self.lab_reset)
        self.lab_btn.place(relwidth=.8, relheight=.122, relx=.1, rely=0.658)
        self.stop_resume()

    def destroy_widget(self):
        try:
            self.lab_frame.destroy()
        except AttributeError as e:
            pass
        self.time_label.destroy()
        self.start_btn.destroy()
        self.lab_btn.destroy()
        self.add_frame= True
        self.lab_array= []
        self.lab_increment = 1
        self.passed= 0
        self.previous_passed = 0

    def stop_resume(self):
        if self.running:
            self.running= False
            self.start_btn.configure(text='resume'.upper())
            self.lab_btn.configure(text='reset'.upper())
        else:
            self.running= True
            self.start_btn.configure(text='stop'.upper())
            self.lab_btn.configure(text='lab'.upper())
            threading.Thread(target=self.stopwatch).start()

    def format_string(self, time_passed):
        secs = time_passed % 60
        min = time_passed // 60
        hrs = min // 60
        return f'{int(hrs):02d}:{int(min):02d}:{int(secs):02d}:{int((time_passed % 1) * 100):02d}'
    def stopwatch(self):
        start = time.time()
        if self.started:
            until_now = self.passed
        else:
            self.started = True
            until_now = 0

        while self.running:
            self.passed= time.time() - start + until_now
            self.time_label.configure(text=self.format_string(self.passed))


    def lab_reset(self):
        if self.running:
            self.lab_array.append(f' Lab {self.lab_increment}   {self.format_string(self.passed)}\n')
            self.lab_increment += 1
            self.previous_passed = self.passed
            if self.add_frame:
                self.lab_frame = customtkinter.CTkTextbox(master=self, wrap=WORD, text_font=("Calibri ", 15), state=DISABLED)
                self.lab_frame.place(rely=.27, relx=.1, relwidth=.8, relheight=.35)

                # Creating of scrollbar
                self.scrollbar = customtkinter.CTkScrollbar(self.lab_frame, command=self.lab_frame.yview)
                self.scrollbar.grid(row=0, column=1, sticky="ns")
                # Configure scrollbar
                self.lab_frame.configure(yscrollcommand=self.scrollbar.set)
                # self.scrollbar.set

                self.add_frame= False
                self.lab_frame.configure(state=NORMAL)
                self.lab_frame.insert(1.0, self.lab_array[0])
                self.lab_frame.configure(state=DISABLED)

            else:
                self.lab_frame.configure(state= NORMAL)
                self.lab_frame.delete(1.0, END)
                for i in self.lab_array:
                    self.lab_frame.insert(1.0, i)
                self.lab_frame.configure(state= DISABLED)

        else:
            self.destroy_widget()
            self.on_start()



    def build(self):
        self.geometry('311x284')
        self.title('Stop Watch')
        self.resizable(0,0)
        self.on_start()
        self.mainloop()

if __name__ == '__main__':
    StopWatch().build()

# Lab   00:00:00.00       l