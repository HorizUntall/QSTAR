import pandas as pd
import io
import matplotlib
matplotlib.use('Agg') # Crucial: forces matplotlib to run in the background without opening GUI windows
import matplotlib.pyplot as plt

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

class ExportService:
    @staticmethod
    def generate_excel(db_data):
        """
        Creates a multi-sheet Excel file in memory.
        db_data expects a dictionary: {'history': [], 'users': [], 'faculty': []}
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if db_data.get('history'):
                df_history = pd.DataFrame(db_data['history'])
                df_history.to_excel(writer, sheet_name='Attendance History', index=False)
            
            if db_data.get('users'):
                df_users = pd.DataFrame(db_data['users'])
                df_users.to_excel(writer, sheet_name='Registered Users', index=False)
                
            if db_data.get('faculty'):
                df_faculty = pd.DataFrame(db_data['faculty'])
                df_faculty.to_excel(writer, sheet_name='Registered Faculty', index=False)
                
        return output.getvalue()

    # ==========================================
    # Legacy-Adapted Chart Generation Methods
    # ==========================================
    @staticmethod
    def _addlabels(ax, x, y, size, scale):
        for i in range(len(x)):
            # Placed text slightly above the bar for readability
            ax.text(i, y[i], str(y[i]), ha='center', va='bottom', fontsize=size*scale)

    @staticmethod
    def _create_lineGraph(x, y, title='Line Graph', xlabel='X-label', ylabel='Y-label', scale=1):
        fig, ax = plt.subplots(figsize=(6.58031496*scale, 2.4350394*scale)) 
        ax.plot(x, y, marker='o') # Added dots to the line graph for clarity

        ax.set_title(title, fontsize=12*scale, fontname="Helvetica")
        ax.set_xlabel(xlabel, fontsize=10*scale, fontname="Helvetica")
        ax.set_ylabel(ylabel, fontsize=10*scale, fontname="Helvetica")

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.tick_params(axis='x', labelrotation=45)
        plt.xticks(fontsize=8*scale, fontname="Helvetica")
        plt.yticks(fontsize=8*scale, fontname="Helvetica")

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2, dpi=200)
        plt.close(fig)
        buf.seek(0)
        return ImageReader(buf)

    @staticmethod
    def _create_barGraph(x, y, title='Bar Graph', xlabel='X-label', ylabel='Y-label', scale=1):
        # Ensure we have data, otherwise provide a dummy empty state
        if not x: x, y = ["No Data"], [0]

        fig, ax = plt.subplots(figsize=(6.58031496*scale, 2.4350394*scale))
        ax.bar(x, y)

        ax.set_title(title, fontsize=12*scale, fontname="Helvetica")
        ax.set_xlabel(xlabel, fontsize=10*scale, fontname="Helvetica")
        ax.set_ylabel(ylabel, fontsize=10*scale, fontname="Helvetica")
        
        plt.xticks(fontsize=8*scale, fontname="Helvetica")
        plt.yticks(fontsize=8*scale, fontname="Helvetica")
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ExportService._addlabels(ax, x, y, size=8, scale=scale)
        ax.tick_params(axis='x', labelrotation=10)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2, dpi=200)
        plt.close(fig)
        buf.seek(0)
        return ImageReader(buf)

    @staticmethod
    def _create_pieGraph(labels, values, title='Pie Graph', scale=1):
        fig, ax = plt.subplots(figsize=(6.58031496*scale, 2.4350394*scale))

        mycolors = ['#EE649E', '#4687E5']
        
        if sum(values) == 0:
            ax.pie([100], labels=['None'], colors=['#D3D3D3'], textprops={'fontsize': 8*scale})
        else:
            ax.pie(values, labels=labels, colors=mycolors, autopct='%.1f%%', textprops={'fontsize': 8*scale})

        plt.suptitle('GAD Statistics', y=1.05, fontsize=10*scale, fontname="Helvetica")
        plt.title(f'Out of all {sum(values)} visits', fontsize=8*scale, fontname="Helvetica")
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2, dpi=200)
        plt.close(fig)
        buf.seek(0)
        return ImageReader(buf)

    # ==========================================
    # Main PDF Generation
    # ==========================================
    @staticmethod
    def generate_pdf(dashboard_data, start_date=None, end_date=None):
        """
        Creates a PDF report containing generated matplotlib charts.
        """
        # 1. Prepare Data for Charts
        visits = dashboard_data.get('visits_vs_time', [])
        x_time = [str(v['visit_date']) for v in visits]
        y_time = [v['frequency'] for v in visits]

        goers = dashboard_data.get('top_goers', [])
        x_goers = [f"{g['first_name']} {g['last_name'][0]}." for g in goers] # Shortened name to fit chart
        y_goers = [g['total_visits'] for g in goers]

        batches = dashboard_data.get('batch_visits', [])
        x_batch = [b['batch'] for b in batches]
        y_batch = [b['frequency'] for b in batches]

        gender = dashboard_data.get('gender', {})
        total_visits = gender.get('total_visits', 0)
        male_count = int(total_visits * (gender.get('male_pct', 0) / 100))
        female_count = int(total_visits * (gender.get('female_pct', 0) / 100))

        kpis = dashboard_data.get('kpis', {})
        avg_time_hrs = round(kpis.get('avg_time_spent_minutes', 0) / 60, 2)
        avg_visits_day = kpis.get('avg_visits_per_day', 0)

        # 2. Generate Image Buffers
        graph1_scale, graph2_scale, graph3_scale, graph4_scale = 1, 0.6, 1, 0.6

        img_line = ExportService._create_lineGraph(x_time, y_time, 'Frequency over Time', 'Time', 'Frequency', graph1_scale)
        img_bar1 = ExportService._create_barGraph(x_goers, y_goers, 'Top Clients', 'Clients', 'Frequency', graph2_scale)
        img_pie = ExportService._create_pieGraph([f'Female\n{female_count}', f'Male\n{male_count}'], [female_count, male_count], 'GAD Statistics', graph3_scale)
        img_bar2 = ExportService._create_barGraph(x_batch, y_batch, 'Frequency per Batch', 'Batch', 'Frequency', graph4_scale)

        # 3. Build the PDF Layout
        output = io.BytesIO()
        pdf = canvas.Canvas(output, pagesize=A4)
        w, h = A4

        MARGIN = 50

        # Replace "Helvetica-Bold" and "Helvetica" with "TNR-B" and "TNR" if you register the legacy fonts!
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(MARGIN, h - MARGIN, "Q-STAR REPORT")

        pdf.setFont("Helvetica", 10)
        time_range_str = f"{start_date or 'Start'} --- {end_date or 'Present'}"
        x_pos = w - MARGIN - pdf.stringWidth(time_range_str, "Helvetica", 10) 
        pdf.drawString(x_pos, h - MARGIN, time_range_str)

        pdf.line(MARGIN, h - MARGIN - 10, w - MARGIN, h - MARGIN - 10)

        pdf.setFont("Helvetica", 15)
        pdf.drawString(MARGIN, h - MARGIN - 40, "Data Summary")

        # Draw line graph
        linegraph_y = h - MARGIN - 80 - 2.4350394 * 72
        pdf.drawImage(img_line, (w/2)-(6.58031496*72/2), linegraph_y, preserveAspectRatio=True, mask='auto', width=6.58031496*72, height=2.4350394*72)

        # Draw Bar Graph Top Clients
        bargraph1_y = linegraph_y - 30 - 2.4350394 * graph2_scale * 72
        pdf.drawImage(img_bar1, -20, bargraph1_y, preserveAspectRatio=True, mask='auto', width=6.58031496*graph2_scale*72, height=2.4350394*graph2_scale*72)

        # Draw GAD STATS
        gadgraph_y = bargraph1_y
        pdf.drawImage(img_pie, (w/2)-6.58031496*graph3_scale*72/8, gadgraph_y+10, preserveAspectRatio=True, mask='auto', width=6.58031496*graph3_scale*72, height=2.4350394*graph3_scale*72)

        # Draw Bar Graph Top Batches
        bargraph2_y = bargraph1_y - 30 - 2.4350394 * graph4_scale * 72
        pdf.drawImage(img_bar2, -20, bargraph2_y+10, preserveAspectRatio=True, mask='auto', width=6.58031496*graph4_scale*72, height=2.4350394*graph4_scale*72)

        # Draw Other Stats
        pdf.setFont("Helvetica", 12)
        otherstats_heading_y = bargraph2_y + 2.4350394 * graph4_scale * 72 - 10
        otherstats_x = (w/2) + 70
        pdf.drawString(otherstats_x, otherstats_heading_y, "Other Statistics")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(otherstats_x, otherstats_heading_y - 20, f"Average time spent: {avg_time_hrs} hrs")
        pdf.drawString(otherstats_x, otherstats_heading_y - 40, f"Avg visits per day: {avg_visits_day}")
        pdf.drawString(otherstats_x, otherstats_heading_y - 60, f"Total visits: {total_visits}")

        pdf.save()
        return output.getvalue()