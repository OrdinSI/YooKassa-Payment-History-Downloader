import csv
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox
from yookassa import Configuration, Payment


config_account_id_1 = 'shopId'
config_secret_key_1 = 'secret_key'

config_account_id_2 = 'shopId'
config_secret_key_2 = 'secret_key'

accounts = [
    {'id': config_account_id_1, 'key': config_secret_key_1},
    {'id': config_account_id_2, 'key': config_secret_key_2},
]


def upload_payments(account_id, secret_key, start_date_iso, end_date_iso):
    Configuration.account_id = account_id
    Configuration.secret_key = secret_key

    payments = []
    limit = 100
    cursor = None

    # Цикл для перебора страниц платежей
    while True:
        params = {
            'created_at.gte': start_date_iso,
            'created_at.lte': end_date_iso,
            'limit': limit
        }

        if cursor:
            params['cursor'] = cursor

        payment_list = Payment.list(params)

        # Обработка текущей страницы платежей
        for payment in payment_list.items:
            if payment.status == 'succeeded':
                payments.append({
                    'Payment ID': payment.id,
                    'Status': payment.status,
                    'Income_amount': payment.income_amount.value,
                    'Currency': payment.income_amount.currency,
                    'Created_at': payment.created_at,
                    'Captured_at': payment.captured_at
                })

        # Проверяем, есть ли следующая страница
        if payment_list.next_cursor:
            cursor = payment_list.next_cursor
        else:
            break

    return payments


def write_to_csv(filename, data):
    full_path = os.path.join(os.getcwd(), filename)
    file_exists = os.path.isfile(full_path)
    with open(full_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)


def fetch_data():
    start_date_str = start_date_entry.get()
    end_date_str = end_date_entry.get()

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        start_date_iso = start_date.isoformat()
        end_date_iso = end_date.isoformat()

        all_payments = []

        for account in accounts:  # Итерация по списку accounts
            account_id = account['id']
            secret_key = account['key']
            payments_data = upload_payments(account_id, secret_key, start_date_iso, end_date_iso)
            if payments_data:
                all_payments.extend(payments_data)

        if all_payments:
            # Показываем диалоговое окно для сохранения файла
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            )
            if filepath:  # Проверяем, что пользователь выбрал файл
                write_to_csv(filepath, all_payments)
                messagebox.showinfo("Success", f"Data fetched and written to {filepath} successfully.")
        else:
            messagebox.showinfo("No Data", "No payments were found for the specified period.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid date format. Please enter dates in YYYY-MM-DD format. {e}")


# Создание основного окна Tkinter
root = tk.Tk()
root.title("Payment Data Fetcher")
root.geometry("300x100")

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0)
tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=1, column=0)

start_date_entry = tk.Entry(root)
end_date_entry = tk.Entry(root)
start_date_entry.grid(row=0, column=1)
end_date_entry.grid(row=1, column=1)

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=2, column=0, columnspan=2)

root.mainloop()
