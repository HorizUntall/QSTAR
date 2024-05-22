import json
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class ReportMaker:
    def __init__(self, filepath="web/report/processed_data.json"): 
        self.filepath = filepath
        self.csfont = {'fontname':'Times New Roman'}
        self.graph1_scale = 1 # Frequency over Time
        self.graph2_scale = 0.6 # Top Clients
        self.graph3_scale = 1 # GAD Stats
        self.graph4_scale = 0.6 # Top Batches

    def update_json(self, processed_list, category):
        try:
            with open(self.filepath, "r") as jsonFile:
                data = json.load(jsonFile)
            
            data[category] = processed_list
            
            with open(self.filepath, "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)
        except:
            with open(self.filepath, "w") as jsonFile:
                json.dump({}, jsonFile, indent=4)

    def addlabels(self, x,y,size,scale):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha = 'center', fontsize=size*scale)
    
    def create_lineGraph(self, independent=[], dependent=[], title='Line Graph', xlabel='X-label', ylabel='Y-label', scale=1):
        fig, ax = plt.subplots(figsize=(6.58031496*scale, 2.4350394*scale)) 
        ax.plot(independent, dependent)

        #adds a title and axes labels
        ax.set_title(title, fontsize=12*scale, **self.csfont)
        ax.set_xlabel(xlabel, fontsize=10*scale, **self.csfont)
        ax.set_ylabel(ylabel, fontsize=10*scale, **self.csfont)

        #removing top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set ticks and labels
        ax.plot(independent, dependent)
        ax.tick_params(axis='x', labelrotation=45)
        plt.xticks(fontsize=8*scale, **self.csfont)
        plt.yticks(fontsize=8*scale, **self.csfont)

        plt.savefig(f"web/report/{title}.png", bbox_inches='tight' ,pad_inches=0.2, dpi=200)

    def create_barGraph(self, independent=[0], dependent=[0], title='Bar Graph', xlabel='X-label', ylabel='Y-label', scale=1):
        fig, ax = plt.subplots(figsize=(6.58031496*scale, 2.4350394*scale))
        ax.bar(independent, dependent)

        #adds a title and axes labels
        ax.set_title(title, fontsize=12*scale, **self.csfont)
        ax.set_xlabel(xlabel, fontsize=10*scale, **self.csfont)
        ax.set_ylabel(ylabel, fontsize=10*scale, **self.csfont)
        plt.xticks(fontsize=8*scale, **self.csfont)
        plt.yticks(fontsize=8*scale, **self.csfont)
        
        #removing top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        self.addlabels(independent, dependent, size=8, scale=scale)
        ax.tick_params(axis='x', labelrotation=10)

        plt.savefig(f"web/report/{title}.png", bbox_inches='tight', pad_inches=0.2, dpi=200)

    def create_pieGraph(self, independent=[0], dependent=[0], title='Bar Graph', scale=1):
        fig, ax = plt.subplots(figsize=(6.58031496*scale, 2.4350394*scale))

        mycolors = ['#EE649E', '#4687E5']
        ax.pie(independent, labels = dependent, colors = mycolors, autopct='%.1f%%', textprops={'fontsize': 8*scale})

        plt.suptitle('GAD Statistics', y=1.05, fontsize=10*scale, **self.csfont)
        plt.title(f'Out of all {sum(independent)} clients', fontsize=8*scale, **self.csfont)
        
        plt.savefig(f"web/report/{title}.png", bbox_inches='tight', pad_inches=0.2, dpi=200)

    def create_pdf_with_text_image(self, filename, text_stats, scale, time_range):
        image_path = ['web/report/Frequency over Time.png', 'web/report/Top Clients.png', 'web/report/GAD Statistics.png', 'web/report/Frequency per Batch.png']

        # Create a PDF canvas
        pdf = canvas.Canvas(filename, pagesize=A4)

        # # Set document title
        # pdf.setTitle(title)

        # Define margins and font size
        MARGIN = 50
        TITLE_SIZE = 18
        HEADING1 = 15
        HEADING2 = 12
        TEXT = 10

        # registering fonts
        pdfmetrics.registerFont(TTFont('TNR', 'web/font/Times New Roman/TNR.ttf'))
        pdfmetrics.registerFont(TTFont('TNR-I', 'web/font/Times New Roman/TNR-I.ttf'))
        pdfmetrics.registerFont(TTFont('TNR-B', 'web/font/Times New Roman/TNR-B.ttf'))
        pdfmetrics.registerFont(TTFont('TNR-BI', 'web/font/Times New Roman/TNR-BI.ttf'))

        # page dimensions
        w,h = A4

        # Draw title
        pdf.setFont("TNR-B", TITLE_SIZE)
        pdf.drawString(MARGIN , h - MARGIN, "Q-STAR REPORT")

        # Draw time range
        pdf.setFont("TNR", TEXT)
        time_range = f"{time_range[0]} --- {time_range[1]}"
        x_pos = w - MARGIN - pdf.stringWidth(time_range)  # Calculate x-position for right alignment
        pdf.drawString(x_pos, h - MARGIN, time_range)

        line_x1, line_y1, line_x2, line_y2 = MARGIN, h - MARGIN - 10 , w - MARGIN, h - MARGIN - 10
        pdf.line(line_x1, line_y1, line_x2, line_y2)

        # Draw Report Type Title
        pdf.setFont("TNR", HEADING1)
        pdf.drawString(MARGIN , h - MARGIN - 40, "Data Summary")

        # Draw line graph
        linegraph_y = h - MARGIN - 80 - 2.4350394*72
        pdf.drawImage(image_path[0], (w/2)-(6.58031496*72/2), linegraph_y, preserveAspectRatio=True, mask='auto', width=6.58031496*72, height=2.4350394*72)


        # Draw Bar Graph Top Clients
        bargraph1_y = linegraph_y - 30 - 2.4350394*scale*72
        pdf.drawImage(image_path[1], 0-20, bargraph1_y, preserveAspectRatio=True, mask='auto', width=6.58031496*scale*72, height=2.4350394*scale*72)

        # Draw GAD STATS
        gadgraph_y = bargraph1_y
        pdf.drawImage(image_path[2], (w/2)-6.58031496*scale*72/8, gadgraph_y+10, preserveAspectRatio=True, mask='auto', width=6.58031496*scale*72, height=2.4350394*scale*72)

        # Draw Bar Graph Top Batches
        bargraph2_y = bargraph1_y - 30 - 2.4350394*scale*72
        pdf.drawImage(image_path[3], 0-20, bargraph2_y+10, preserveAspectRatio=True, mask='auto', width=6.58031496*scale*72, height=2.4350394*scale*72)

        # Draw Other Stats
        pdf.setFont("TNR", HEADING2)
        otherstats_heading_y = bargraph2_y+2.4350394*scale*72-10
        otherstats_x = (w/2)+70
        pdf.drawString(otherstats_x, otherstats_heading_y, "Other Statistics")

        pdf.setFont("TNR", TEXT)
        otherstats1_y = otherstats_heading_y - 20
        pdf.drawString(otherstats_x, otherstats1_y, f"Average time spent in the library: {text_stats[0]}hrs")

        otherstats2_y = otherstats_heading_y - 40
        pdf.drawString(otherstats_x, otherstats2_y, f"Average number of visits per day: {text_stats[1]}")

        otherstats3_y = otherstats_heading_y - 60
        pdf.drawString(otherstats_x, otherstats3_y, f"Total number of visits: {text_stats[2]}")

        pdf.save()

    def create_report(self):
        # get all data
        with open(self.filepath, "r") as jsonFile:
            data = json.load(jsonFile)

            visitstime = [data['visitsTime'][2], data['visitsTime'][1]]
            time_range = [data['visitsTime'][2][0], data['visitsTime'][2][-1]]
            rankstudents = [data['rankstudents'][0], data['rankstudents'][1]]
            female_count, male_count = data['GAD'][0], data['GAD'][1]
            gadstats = [[female_count, male_count], [f'Female\n{female_count}', f'Male\n{male_count}']]
            rankbatch = [data['visitsBatch'][0], data['visitsBatch'][1]]
            otherstats = [data['average_time'], data['visitsTime'][3], data['visitsTime'][4], time_range] # [avgtime, avgvisitsday, totalvisits, timerange]

        # FREQUENCY OVER TIME
        self.create_lineGraph(independent=visitstime[0], dependent=visitstime[1], title='Frequency over Time', xlabel='Time', ylabel='Frequency', scale=self.graph1_scale)

        # STUDENTS RANKED
        self.create_barGraph(independent=rankstudents[0], dependent=rankstudents[1], title='Top Clients', xlabel='Clients', ylabel='Frequency', scale=self.graph2_scale)

        # GAD STATS
        self.create_pieGraph(independent=gadstats[0], dependent=gadstats[1], title='GAD Statistics', scale=self.graph3_scale)

        # BATCHES RANKED
        self.create_barGraph(independent=rankbatch[0], dependent=rankbatch[1], title='Frequency per Batch', xlabel='Batch', ylabel='Frequency', scale=self.graph4_scale)

        self.create_pdf_with_text_image('web/report/QSTAR-Report.pdf', otherstats, 1, time_range)

# report = ReportMaker()
# report.create_report()

