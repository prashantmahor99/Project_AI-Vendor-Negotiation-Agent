import customtkinter as ctk
import threading
import os

# -----------------------------
# Theme
# -----------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Procurement Agent")

        self.geometry("1500x900")

        self.minsize(1400, 850)

        self.configure(fg_color="#181818")

        self.create_sidebar()

        self.create_header()

        self.create_main_container()

        self.create_dashboard()

        self.create_vendor_panel()

        self.create_summary_cards()

        self.create_rfq_form()

        self.create_workflow()

        self.create_logs()

        self.create_progress()

        self.add_log("Mail Sent")

        self.update_status("Mail Sent")

        self.update_progress(20)

        self.create_controls()

        self.stop_requested = False

    # ----------------------------------
    # Sidebar
    # ----------------------------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(

            self,

            width=240,

            corner_radius=0,

            fg_color="#202020"

        )

        self.sidebar.pack(

            side="left",

            fill="y"

        )

        logo = ctk.CTkLabel(

            self.sidebar,

            text="🤖\nAI PROCUREMENT",

            font=("Segoe UI",24,"bold")

        )

        logo.pack(

            pady=(30,40)

        )

        menu = [

            "🏠 Dashboard",

            "👥 Vendors",

            "📄 Reports",

            "⚙ Settings",

            "❌ Exit"

        ]

        for item in menu:

            btn = ctk.CTkButton(

                self.sidebar,

                text=item,

                height=45,

                corner_radius=8,

                fg_color="#2B2B2B",

                hover_color="#1F6AA5"

            )

            btn.pack(

                padx=20,

                pady=10,

                fill="x"

            )

    # ----------------------------------
    # Header
    # ----------------------------------

    def create_header(self):

        self.header = ctk.CTkFrame(

            self,

            height=70,

            fg_color="#252525",

            corner_radius=0

        )

        self.header.pack(

            side="top",

            fill="x"

        )

        title = ctk.CTkLabel(

            self.header,

            text="AI PROCUREMENT AGENT",

            font=("Segoe UI",28,"bold")

        )

        title.pack(

            side="left",

            padx=25,

            pady=15

        )

        version = ctk.CTkLabel(

            self.header,

            text="Version 1.0",

            font=("Segoe UI",14)

        )

        version.pack(

            side="right",

            padx=25

        )

        self.status = ctk.CTkLabel(

        self.header,

        text="🟢 Ready",

        font=("Segoe UI",16,"bold")

    )

        self.status.pack(
            side="right",
            padx=30
        )    

    # ----------------------------------
    # Main Container
    # ----------------------------------

    def create_main_container(self):

        self.main = ctk.CTkFrame(

            self,

            fg_color="#181818"

        )

        self.main.pack(

            expand=True,

            fill="both",

            padx=20,

            pady=20

        )
    
    def create_dashboard(self):

        self.left_panel = ctk.CTkFrame(
        self.main,
        fg_color="#181818"
    )

        self.left_panel.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0,10)
    )

        self.right_panel = ctk.CTkFrame(
        self.main,
        width=350,
        fg_color="#181818"
    )

        self.right_panel.pack(
        side="right",
        fill="y"
    )    
    def create_rfq_form(self):

        frame = ctk.CTkFrame(
            self.left_panel,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=10
        )

        title = ctk.CTkLabel(
            frame,
            text="📄 RFQ Details",
            font=("Segoe UI",22,"bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.product = ctk.CTkEntry(
            frame,
            placeholder_text="Product Name",
            height=40
        )

        self.product.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.qty = ctk.CTkEntry(
            frame,
            placeholder_text="Quantity",
            height=40
        )

        self.qty.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.budget = ctk.CTkEntry(
            frame,
            placeholder_text="Budget",
            height=40
        )

        self.budget.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.spec = ctk.CTkTextbox(
            frame,
            height=120
        )

        self.spec.pack(
            fill="x",
            padx=20,
            pady=10
        )    
    def create_vendor_panel(self):

        frame = ctk.CTkFrame(
            self.right_panel,
            corner_radius=12
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        title = ctk.CTkLabel(
            frame,
            text="👥 Vendors",
            font=("Segoe UI",20,"bold")
        )

        title.pack(
            pady=15
        )

        self.vendor_list = ctk.CTkTextbox(
            frame,
            width=300
        )

        self.vendor_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.vendor_list.insert(
            "end",
            "Dell\nHP\nLenovo\nAcer"
        )
    def create_summary_cards(self):

        frame = ctk.CTkFrame(
            self.left_panel,
            fg_color="#181818"
        )

        frame.pack(
            fill="x",
            pady=10
        )

        self.best_vendor = ctk.CTkFrame(
            frame,
            height=120,
            corner_radius=12
        )

        self.best_vendor.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        lbl = ctk.CTkLabel(
            self.best_vendor,
            text="🏆 Best Vendor\n---",
            font=("Segoe UI",20,"bold")
        )

        lbl.pack(
            pady=30
        )

        self.lowest_price = ctk.CTkFrame(
            frame,
            height=120,
            corner_radius=12
        )

        self.lowest_price.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        lbl2 = ctk.CTkLabel(
            self.lowest_price,
            text="💰 Lowest Price\n₹0",
            font=("Segoe UI",20,"bold")
        )

        lbl2.pack(
            pady=30
        )

    def create_workflow(self):

        frame = ctk.CTkFrame(
            self.right_panel,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=10
        )

        title = ctk.CTkLabel(
            frame,
            text="⚙ Workflow Status",
            font=("Segoe UI",20,"bold")
        )

        title.pack(
            pady=10
        )

        self.workflow_labels = {}

        steps = [

            "RFQ Created",

            "Mail Sent",

            "Waiting Quotations",

            "Reading Quotations",

            "Comparison",

            "Negotiation Round 1",

            "Negotiation Round 2",

            "Negotiation Round 3",

            "Final Report"

        ]

        for step in steps:

            lbl = ctk.CTkLabel(

                frame,

                text="⚪ " + step,

                anchor="w",

                font=("Segoe UI",15)

            )

            lbl.pack(

                fill="x",

                padx=15,

                pady=3

            )

            self.workflow_labels[step] = lbl    

    def create_progress(self):

        frame = ctk.CTkFrame(

            self.left_panel,

            corner_radius=12

        )

        frame.pack(

            fill="x",

            pady=10

        )

        lbl = ctk.CTkLabel(

            frame,

            text="📊 Progress",

            font=("Segoe UI",18,"bold")

        )

        lbl.pack(

            pady=(10,5)

        )

        self.progress = ctk.CTkProgressBar(

            frame,

            height=18

        )

        self.progress.pack(

            fill="x",

            padx=20,

            pady=15

        )

        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(

            frame,

            text="0%"
       )

        self.progress_label.pack(
            pady=(0,10)
        )        
    
    def create_logs(self):

        frame = ctk.CTkFrame(

            self.left_panel,

            corner_radius=12

        )

        frame.pack(

            fill="both",

            expand=True,

            pady=10

        )

        lbl = ctk.CTkLabel(

            frame,

            text="📜 Live Logs",

            font=("Segoe UI",20,"bold")

        )

        lbl.pack(

            pady=10

        )

        self.logs = ctk.CTkTextbox(

            frame,

            height=250

        )

        self.logs.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )

    def add_log(self, text):

        from datetime import datetime

        time = datetime.now().strftime("%H:%M:%S")

        self.logs.insert(

            "end",

            f"[{time}] {text}\n"

        )

        self.logs.see("end")    

    def update_progress(self, value):

        self.progress.set(value/100)

        self.progress_label.configure(

            text=f"{value}%"

        )    

    def update_status(self, step):

        if step in self.workflow_labels:

            self.workflow_labels[step].configure(

                text="🟢 " + step,

                text_color="#00FF66"

            )

    def create_controls(self):

        frame = ctk.CTkFrame(
            self.left_panel,
            corner_radius=12
        )

        frame.pack(
            fill="x",
            pady=10
        )

        self.start_btn = ctk.CTkButton(
            frame,
            text="▶ Start Procurement",
            height=45,
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.start_procurement
        )

        self.start_btn.pack(
            side="left",
            expand=True,
            padx=10,
            pady=15
        )

        self.stop_btn = ctk.CTkButton(
            frame,
            text="⏹ Stop",
            height=45,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.stop_procurement
        )

        self.stop_btn.pack(
            side="left",
            expand=True,
            padx=10
        )

        self.report_btn = ctk.CTkButton(
            frame,
            text="📂 Open Report",
            height=45,
            command=self.open_report
        )

        self.report_btn.pack(
            side="left",
            expand=True,
            padx=10
        )

    def start_procurement(self):

        self.stop_requested = False

        thread = threading.Thread(

            target=self.procurement_flow,

            daemon=True

        )

        thread.start()

    def stop_procurement(self):

        self.stop_requested = True

        self.status.configure(

            text="🟠 Stopping..."

        )

        self.add_log("Stopping Procurement...")

    def open_report(self):

        file = "output/Price_Comparison.xlsx"

        if os.path.exists(file):

            os.startfile(file)

        else:

            self.add_log("Report Not Found")






if __name__ == "__main__":

    app = Dashboard()

    app.mainloop()            