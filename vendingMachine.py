import PySimpleGUI as sg
from PIL import Image
import os
from datetime import datetime
import csv

def get_current_datetime():
    # Get the current date and time
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

basket = {}
total_quantity = 0
total_price = 0
cash_insert_left = 0
sum_cash = 0
change_dict = {}

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    original_image.thumbnail(size)
    original_image.save(output_image_path)

def add_to_basket(product_key, pro_price, pro_img):
    global total_quantity
    global total_price
    global cash_insert_left

    pro_img = "resized-img-s/"+pro_img

    # Ensure product key exists in basket
    if product_key not in basket:
        basket[product_key] = {"quantity": 0, "price": 0, "img":""}  # Initialize dictionary

    # Update product details
    basket[product_key]["price"] = int(pro_price)  # Store price as integer
    basket[product_key]["quantity"] += 1  # Increase quantity
    basket[product_key]["img"] = pro_img   # Product Image

    # Calculate total price and quantity
    total_price = sum(item["price"] * item["quantity"] for item in basket.values())
    total_quantity = sum(item["quantity"] for item in basket.values())
    cash_insert_left = total_price

    # Update UI
    window["-TOTAL-"].update(total_quantity)
    # update_basket_display()

    print("Total price",total_price)  # Debugging line

def reset_purchase():
    global basket
    global total_quantity
    global total_price

    global sum_cash
    global cash_change
    global cash_insert_left
    global change_dict

    basket = {}
    total_quantity = 0 
    total_price = 0
    sum_cash = 0
    cash_change = 0
    cash_insert_left = 0 
    change_dict = {}

def sum_price(pro_price):
    global total_price
    global cash_insert_left

    print(pro_price)
    total_price += int(pro_price)
    cash_insert_left = total_price
    return total_price

def sum_insert_money(money):
    global sum_cash, cash_insert_left, cash_change

    money = int(money)  # Convert input to integer
    sum_cash += money   # Add inserted money to total cash inserted

    if sum_cash >= total_price:  # If enough or more money is inserted
        cash_change = sum_cash - total_price  # Calculate change
        cash_insert_left = 0  # No more money needs to be inserted
        print(f"Total cash inserted: {sum_cash}")
        print(f"Cash Change: {cash_change}")

        accept_money_window['-CASH-INSERT-LEFT-'].update(0)
        give_change(cash_change)  # Function to dispense change

    else:  # If more money is still needed
        cash_insert_left = total_price - sum_cash  # Update remaining amount
        print(f"Total cash inserted: {sum_cash}")
        print(f"Cash Insert left: {cash_insert_left}")

        accept_money_window['-CASH-INSERT-LEFT-'].update(cash_insert_left)


def give_change(amount):
    denominations = [1000, 500, 100, 50, 20, 10, 5, 2, 1]  # Thai Baht denominations
    global change_dict

    for denom in denominations:
        if amount >= denom:
            count = amount // denom  # Get number of bills/coins for this denomination
            amount -= count * denom  # Reduce the remaining amount
            change_dict[denom] = count  # Store result

    print("\n💰 Change to be given:")
    for denom, count in change_dict.items():
        print(f"{denom} บาท: {count} ใบ/เหรียญ")

    return change_dict

def save_purchase_log():
    # Save to text file
    with open("purchase_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Date and Time: {get_current_datetime()}\n")
        log_file.write("Items Purchased:\n")
        
        for key, item in basket.items():
            log_file.write(f"Product: {key}, Quantity: {item['quantity']}, Price per item: {item['price']}\n")
        
        log_file.write(f"Total Quantity: {total_quantity}\n")
        log_file.write(f"Total Price: {total_price}\n")
        log_file.write(f"Cash Inserted: {sum_cash}\n")
        log_file.write(f"Change: {cash_change}\n")
        log_file.write("-" * 50 + "\n")  # Separator for readability

    # Save to CSV file
    with open("purchase_log.csv", "a", newline='', encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # If it's the first entry, write the header
        if csv_file.tell() == 0:
            csv_writer.writerow(["Date and Time", "Product", "Quantity", "Price per item (฿)", "Total Quantity", "Total Price (฿)", "Cash Inserted (฿)", "Change (฿)"])
        
        for key, item in basket.items():
            csv_writer.writerow([get_current_datetime(), key, item['quantity'], item['price'], total_quantity, total_price, sum_cash, cash_change])

with open("product.txt", "r") as f:
    data = [line.strip().split(",") for line in f.readlines()]

# Resize Image ====================================================================================================
input_folder = 'img/'
img_small_output_folder = 'resized-img-s/'
img_large_output_folder = 'resized-img-l/'
s_size = (100,100)
l_size = (150,150)

# Ensure output folder exists
os.makedirs(img_small_output_folder, exist_ok=True)

# Get all image files from the folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):  # Filter image files
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(img_small_output_folder, filename)
        
        resize_image(input_path, output_path, s_size)

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(img_large_output_folder, filename)
        
        resize_image(input_path, output_path, l_size)

print("Resizing completed!")
# Resize Image ====================================================================================================


sg.theme("LightGray1")  # Optional: Set theme

sg.set_options(font=('Roboto', 14))

header_footer_color = 'orange'
h1 = ('Roboto', 22)

# ===================================================================== Components ===========================================================================
def header_component():
    header_layout = [
        [sg.Column(
            [
                [sg.Text('AFTER PARTY BOX', font=('Helvetica', 16), pad=(10, 10), background_color=header_footer_color), sg.Push(background_color=header_footer_color), sg.Text(get_current_datetime(), key="-DATE-TIME-", font=('Helvetica', 12), pad=(10, 10), background_color=header_footer_color)]
            ], 
            background_color=header_footer_color,  # Set the background color for the entire column
            expand_x=True
        )]
    ]
    return header_layout

# ======================================================================== Layouts ========================================================================
def main_layout():

    third = len(data)//3
    column1 = data[:third]
    column2 = data[third:2*third]
    column3 = data[2*third:]

    # Create vertical layout for both columns
    column_layout1 = [ 
        [
            sg.Column([  # Column to group image and product name
                [sg.Image(filename=f"resized-img-s/{item[3]}", size=(100, 100))],  # Image
                [sg.Text(item[1], expand_x=True, justification='c')],  # Product name
                [sg.Text(item[2]),sg.Text("฿")],  # Price Text
                [sg.Button("เพิ่ม", key=item[0])]  # Add button
            ], element_justification='c', pad=(0, 10)),
        ]
        for item in column1
    ]


        
    column_layout2 = [ 
        [
            sg.Column([  # Column to group image and product name
                [sg.Image(filename=f"resized-img-s/{item[3]}", size=(100, 100))],  # Image
                [sg.Text(item[1], expand_x=True, justification='c')],  # Product name
                [sg.Text(item[2]),sg.Text("฿")],  # Price Text
                [sg.Button("เพิ่ม", key=item[0])]  # Add button
            ], element_justification='c', pad=(0, 10)),
        ]
        for item in column2
    ]

    column_layout3 = [ 
        [
            sg.Column([  # Column to group image and product name
                [sg.Image(filename=f"resized-img-s/{item[3]}", size=(100, 100))],  # Image
                [sg.Text(item[1], expand_x=True, justification='c')],  # Product name
                [sg.Text(item[2]),sg.Text("฿")],  # Price Text
                [sg.Button("เพิ่ม", key=item[0])]  # Add button
            ], element_justification='c', pad=(0, 10)),
        ]
        for item in column3
    ]

    # calculate column height
    col_height = 0
    for i in column3:
        col_height+=250

    # Return layout with a vertical arrangement
    return [
        [header_component()],
        [sg.Text('รายการสินค้า')],
        [
            sg.Column([
                [
                    sg.Column(column_layout1, expand_y=True, element_justification='c', pad=(10, 10), size=(200,col_height)),
                    sg.Column(column_layout2, expand_y=True, element_justification='c', pad=(10, 10), size=(200,col_height)),
                    sg.Column(column_layout3, expand_y=True, element_justification='c', pad=(10, 10), size=(200,col_height)),
                ]
        ], size=(600, 400), scrollable=True, expand_x=True, expand_y=True, vertical_scroll_only=True)  # Set size & enable scrolling
    ],
        [sg.Column([
            [sg.Text("สินค้า ",background_color=header_footer_color), sg.Text(total_quantity, key="-TOTAL-", background_color=header_footer_color), sg.Text(" รายการ", background_color=header_footer_color)],
            [sg.Push(background_color=header_footer_color), sg.Button("ไปยังตะกร้า")]
        ], background_color=header_footer_color, expand_x=True)]

    ]
def basket_layout():
            basket_layout = [[header_component()],[sg.Text("Items in Basket:")]]
            
            # Dynamically create a row for each item in the basket
            for key, item in basket.items():
                print(item)
                basket_layout.append([
                    sg.Image(filename=item['img'], size=(100,100)),
                    sg.Text(key, size=(12, 1)),  # Product name
                    sg.Push(),
                    sg.Push(),
                    sg.Text(f"{item['price']}฿", size=(6, 1)),  # Price
                    sg.Push(),
                    sg.Button("-", key=f"-DEC-{key}"),  # Decrease button
                    sg.Push(),
                    sg.Text(str(item['quantity']), size=(5, 1), key=f"-QTY-{key}"),  # Quantity display
                    sg.Button("+", key=f"-INC-{key}"),  # Increase button
                ])
            
            # Add total price and action buttons
            basket_layout.extend([
                [sg.Text('',expand_y=True)],
                [sg.Text("ยอดชำระ"), sg.Push(), sg.Text(f"{total_price} บาท", key="-TOTAL-PRICE-")],
                [sg.Button("เลือกสินค้าเพิ่มเติม"), sg.Push(), sg.Button("ชำระเงิน")]
            ])
            
            return basket_layout
def accept_money_layout():
    money_btn_layout = [
        [sg.Push(), sg.Button('1'),sg.Button('2'),sg.Button('5'),sg.Button('10'),sg.Button('20'), sg.Push()],
        [sg.Push(), sg.Button('50'),sg.Button('100'),sg.Button('500'),sg.Button('1000'), sg.Push()]
    ]

    accept_money_layout = [
        [header_component()],
        [sg.Text('',expand_y=True)],
        [sg.Push(), sg.Image(filename='resized-img-l/insert_cash.png'), sg.Push()],
        [sg.Push(), sg.Text('ยอดชำระ', font=h1), sg.Text(cash_insert_left, key="-CASH-INSERT-LEFT-", font=h1), sg.Text('บาท', font=h1), sg.Push()],
        [sg.Push(), sg.Text('กรุณาหยอดเหรียญ หรือ ธนบัตร'), sg.Push()],
        [sg.Push(), sg.Text('ตามจำนวนเงินที่ต้องชำระ'), sg.Push()],
        [sg.Text('',expand_y=True)],
        money_btn_layout,
        [sg.Button('ย้อนกลับ'), sg.Push(), sg.Button('ยืนยันการชำระ')]
    ]
    return accept_money_layout
def success_purchase_layout():
    header_component()
    change_display = []
    for denom, count in change_dict.items():
        change_display.append([sg.Push(),sg.Text(f"{denom} บาท: {count} ใบ/เหรียญ"),sg.Push()],)

    accept_money_layout = [
        [header_component()],
        [sg.Text('',expand_y=True)],
        [sg.Push(), sg.Image(filename='resized-img-l/thanks-hand.png'), sg.Push()],
        [sg.Push(), sg.Text('ชำระเงินสำเร็จ', font=h1), sg.Push()],
        [sg.Push(), sg.Text('ขอบคุณที่ใช้บริการ', font=h1), sg.Push()],
    ]
    if cash_change != 0:
        accept_money_layout+=[
                [sg.Push(), sg.Text('กรุณารับเงินทอน'), sg.Push()],
                [sg.Push(), sg.Text("เงินทอนรวม "), sg.Text(cash_change), sg.Text(" บาท"), sg.Push()]
            ]
        
    accept_money_layout+=[
        change_display,
        
        [sg.Push(), sg.Text('กรุณารับสินค้าที่ช่องจ่ายสินค้า'), sg.Push()],
        [sg.Text('',expand_y=True)],
        [sg.Push(), sg.Button('เลือกซื้อสินค้า', button_color=('white', 'green'), border_width=0, pad=(20, 10)), sg.Push()]
    ]
    return accept_money_layout

# ======================================================================== Layouts ========================================================================

def create_window(title,layout):
     return sg.Window(title,layout,size=(700,800),finalize=True)

# Start with the main window
window = create_window('Main Menu',main_layout())

while True:
    
    event, values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED:
        break

    window["-DATE-TIME-"].update(get_current_datetime())
    window["-TOTAL-"].update(total_quantity)

    # Listen for button clicks dynamically
    if event in [item[0] for item in data]: 
        product_key = data[int(event)-1]
        print("pro_key",product_key)
        # sg.popup(f"You clicked เพิ่ม on {event}!")
        add_to_basket(product_key[1],product_key[2], product_key[3])
    
    if event == 'ไปยังตะกร้า':
        if basket != {}:
            window.close()
            
            basket_window = create_window('ตะกร้า',basket_layout())

            while True:
                basket_event, basket_values = basket_window.read(timeout=1000)
                if basket_event == sg.WIN_CLOSED:
                    break

                basket_window["-DATE-TIME-"].update(get_current_datetime())

                # Handle increase button (+)
                if basket_event.startswith("-INC-"):
                    product_key = basket_event.replace("-INC-", "")
                    basket[product_key]["quantity"] += 1  # Increase quantity
                    basket_window[f"-QTY-{product_key}"].update(basket[product_key]["quantity"])  # Update UI
                    total_price = sum(item['price'] * item['quantity'] for item in basket.values())  # Recalculate total
                    cash_insert_left = total_price
                    basket_window["-TOTAL-PRICE-"].update(f"{total_price} บาท")  # Update total

                # Handle decrease button (-)
                if basket_event.startswith("-DEC-"):
                    
                    product_key = basket_event.replace("-DEC-", "")
                    
                    if basket[product_key]["quantity"] > 1:
                        basket[product_key]["quantity"] -= 1  # Decrease quantity
                    else:
                        del basket[product_key]  # Remove item if quantity reaches 0
                        total_price = sum(item['price'] * item['quantity'] for item in basket.values())  # Recalculate total
                        basket_window["-TOTAL-PRICE-"].update(f"{total_price} บาท")  # Update total
                        basket_window.close()  # Close and re-create UI to reflect changes
                        basket_window = create_window('ตะกร้า',basket_layout())
                        continue  # Restart loop to avoid errors
                    

                    basket_window[f"-QTY-{product_key}"].update(basket[product_key]["quantity"])  # Update UI
                    total_price = sum(item['price'] * item['quantity'] for item in basket.values())  # Recalculate total
                    cash_insert_left = total_price
                    basket_window["-TOTAL-PRICE-"].update(f"{total_price} บาท")  # Update total

                if basket_event == 'เลือกสินค้าเพิ่มเติม':
                    total_quantity = sum(item["quantity"] for item in basket.values())  
                    basket_window.close()
                    window = create_window('หน้าหลัก',main_layout())
                    break  # Exit the basket window event loop

                if basket != {}:
                    if basket_event == 'ชำระเงิน':
                        print("Total price",total_price)  # Debugging line
                        basket_window.close()
                        accept_money_window = create_window('ชำระเงิน', accept_money_layout())
                        cash_insert_left = total_price
                        print("Cash Insert left : ",cash_insert_left)
                        while True:
                            accept_event, accept_values = accept_money_window.read(timeout=1000)

                            if accept_event == sg.WIN_CLOSED:
                                break

                            accept_money_window["-DATE-TIME-"].update(get_current_datetime())

                            if accept_event == 'ย้อนกลับ':
                                accept_money_window.close()
                                basket_window = create_window('ตะกร้า',basket_layout())
                                break
                            for i in ['1','2','5','10','20','50','100','500','1000']:
                                if accept_event == i:
                                    print("User insert : ",i)
                                    sum_insert_money(i)
                            if cash_insert_left == 0:
                                print("Proceed to successfully purchase")
                                save_purchase_log()
                                accept_money_window.close()
                                success_purchase_window = create_window('สำเร็จ', success_purchase_layout())
                                while True:
                                    sp_event, sp_values = success_purchase_window.read(timeout=1000)

                                    success_purchase_window["-DATE-TIME-"].update(get_current_datetime())

                                    if sp_event == sg.WIN_CLOSED:
                                        break

                                    if sp_event == 'เลือกซื้อสินค้า':
                                        success_purchase_window.close()
                                        window = create_window('หน้าหลัก',main_layout())
                                        reset_purchase()
                                        window["-TOTAL-"].update(total_quantity)
                                        print("Total quantity : ",total_quantity)
                                        break
            basket_window.close()  # Close the basket window
window.close()