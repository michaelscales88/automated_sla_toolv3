def white_wash(client_report=None):  # Clears used data reports after a final report is output
    if client_report is None:
        client_report = []
    print("Clearing data cache.")
    clear_used_data('\\raw\\')
    clear_used_data('\\converted_files_come_here\\Desktop\\development\\Daily SLA Parser - Automated Version\\raw\\')
    if client_report:
        for client in client_report:
            client.reset()

def clear_used_data(folder_to_clear):
    folder = (SELF_PATH + folder_to_clear)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)