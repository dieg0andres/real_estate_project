from tkinter import *
from tkinter import ttk

def dummy(x):
    print(x)

root = Tk()
root.title('Houston Real Estate Intelligence')

search_frame = ttk.Frame(root, width=400, height=600)
search_frame['padding'] = 5
search_frame['borderwidth'] = 2
search_frame['relief'] = 'raised'
search_frame.grid()

min_price_label = ttk.Label(search_frame,text='Price (min) (k$)')
min_price_label.grid(column=1, row=1, sticky='E')
min_price_var = StringVar()
min_price_combobox= ttk.Combobox(search_frame, textvariable=min_price_var, justify='right', state='readonly')
min_price_combobox.option_add('*TCombobox*Listbox.Justify', 'right')
min_price_combobox.bind('<<ComboboxSelected>>', dummy)
min_price_combobox['values']= [format(x,",d") for x in range(100,10**4+100,100)]
min_price_combobox.set('100')
min_price_combobox.unbind_class('TCombobox', '<Mousewheel>')
min_price_combobox.grid(column=2, row=1)

max_price_label = ttk.Label(search_frame,text='Price (max) (k$)')
max_price_label.grid(column=1, row=2, sticky='E')
max_price_var = StringVar()
max_price_combobox= ttk.Combobox(search_frame, textvariable=max_price_var, justify='right', state='readonly')
max_price_combobox.option_add('*TCombobox*Listbox.Justify', 'right')
max_price_combobox.bind('<<ComboboxSelected>>', dummy)
max_price_combobox['values']= [format(x,",d") for x in range(100,10**4+100,100)]
max_price_combobox.set('10,000')
max_price_combobox.unbind_class('TCombobox', '<Mousewheel>')
max_price_combobox.grid(column=2, row=2)



bed_min_label = ttk.Label(search_frame,text='Bedrooms (min)')
bed_min_label.grid(column=1, row=3, sticky='W')

bed_max_label = ttk.Label(search_frame,text='Bedrooms (max)')
bed_max_label.grid(column=1, row=4, sticky='W')

bath_min_label = ttk.Label(search_frame,text='Bathrooms (min)')
bath_min_label.grid(column=1, row=5, sticky='W')

bath_max_label = ttk.Label(search_frame,text='Bathrooms (max)')
bath_max_label.grid(column=1, row=6, sticky='W')

zip_label = ttk.Label(search_frame,text='Zip codes')
zip_label.grid(column=1, row=7, sticky='W')

zip_codes = '77002, 77007, 77008, 77019'
zips = StringVar(value=zip_codes)
zip_listbox = Listbox(search_frame, listvariable=zips, height=5)
zip_listbox.grid(column=2, row=8)





root.mainloop()