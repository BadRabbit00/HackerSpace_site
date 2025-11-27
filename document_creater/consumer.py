import os
import sys
import django
import pika
import json
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from django.core.files import File

# Add the project root to the python path
sys.path.append('/app')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackerSpace.settings')
django.setup()

from inventory.models import Loan
from users.models import User

# Register Fonts
try:
    # Paths for Debian/Ubuntu (Docker image)
    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
    FONT_REGULAR = 'DejaVuSans'
    FONT_BOLD = 'DejaVuSans-Bold'
except Exception as e:
    print(f" [!] Font loading error: {e}. Fallback to Helvetica.")
    FONT_REGULAR = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'

def generate_pdf(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        borrower = loan.borrower
        personal_data = getattr(borrower, 'personal_data', None)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # Header
        p.setFont(FONT_BOLD, 16)
        p.drawString(50, 800, "LOAN AGREEMENT / АКТ ПРИЕМА-ПЕРЕДАЧИ")
        
        p.setFont(FONT_REGULAR, 12)
        p.drawString(50, 770, f"Document ID: {loan.id}")
        p.drawString(50, 750, f"Date (Issue): {loan.taken_at.strftime('%Y-%m-%d') if loan.taken_at else 'PENDING'}")
        p.drawString(50, 730, f"Date (Return): {loan.deadline.strftime('%Y-%m-%d')}")
        
        # Lender Info
        p.setFont(FONT_BOLD, 12)
        p.drawString(50, 690, "LENDER (Владелец):")
        p.setFont(FONT_REGULAR, 12)
        p.drawString(50, 670, "Organization: BlackIce HackerSpace")
        
        try:
            blackice_user = User.objects.get(username='BlackIce')
            lender_bin = blackice_user.personal_data.iin if hasattr(blackice_user, 'personal_data') else "N/A"
            p.drawString(50, 650, f"BIN (БИН): {lender_bin}")
        except User.DoesNotExist:
            p.drawString(50, 650, "BIN (БИН): N/A (User 'BlackIce' not found)")

        # Borrower Info
        p.setFont(FONT_BOLD, 12)
        p.drawString(50, 610, "BORROWER (Получатель):")
        p.setFont(FONT_REGULAR, 12)
        p.drawString(50, 590, f"Username: {borrower.username}")
        if personal_data:
            p.drawString(50, 570, f"Full Name: {personal_data.full_name}")
            p.drawString(50, 550, f"IIN (ИИН): {personal_data.iin}")
        else:
            p.drawString(50, 570, "Full Name: N/A")
            p.drawString(50, 550, "IIN (ИИН): N/A")

        # Item Info
        p.setFont(FONT_BOLD, 12)
        p.drawString(50, 510, "ITEM DETAILS (Предмет):")
        p.setFont(FONT_REGULAR, 12)
        p.drawString(50, 490, f"Name: {loan.item.name}")
        p.drawString(50, 470, f"Inventory #: {loan.item.inventory_number}")
        p.drawString(50, 450, f"Purpose: {loan.purpose}")

        # Signatures
        p.line(50, 350, 250, 350)
        p.drawString(50, 330, "Lender Signature")
        
        p.line(350, 350, 550, 350)
        p.drawString(350, 330, "Borrower Signature")

        # Attached Documents
        if personal_data:
            docs = []
            if personal_data.document_scan_front:
                docs.append(("Front Scan", personal_data.document_scan_front))
            if personal_data.document_scan_back:
                docs.append(("Back Scan", personal_data.document_scan_back))
            if personal_data.student_document:
                docs.append(("Student ID", personal_data.student_document))
            
            if docs:
                p.showPage()
                p.setFont(FONT_BOLD, 14)
                p.drawString(50, 800, "ATTACHED DOCUMENTS / ПРИЛОЖЕНИЯ")
                
                y_pos = 750
                for title, doc_field in docs:
                    try:
                        # Check if file exists
                        if doc_field and hasattr(doc_field, 'path') and os.path.exists(doc_field.path):
                            p.setFont(FONT_BOLD, 12)
                            p.drawString(50, y_pos, title)
                            # Draw image
                            # Maintain aspect ratio, max width 500, max height 300
                            p.drawImage(doc_field.path, 50, y_pos - 310, width=500, height=300, preserveAspectRatio=True, anchor='nw')
                            y_pos -= 350
                            
                            if y_pos < 100:
                                p.showPage()
                                y_pos = 750
                    except Exception as img_err:
                        print(f" [!] Error adding image {title}: {img_err}")
                        p.drawString(50, y_pos, f"Error loading {title}")
                        y_pos -= 50

        p.showPage()
        p.save()
        
        buffer.seek(0)
        filename = f"loan_{loan.id}_contract.pdf"
        
        # Save to model
        loan.contract_file.save(filename, File(buffer), save=True)
        print(f" [x] Generated PDF for Loan {loan.id}")
        
    except Loan.DoesNotExist:
        print(f" [!] Loan {loan_id} not found")
    except Exception as e:
        print(f" [!] Error generating PDF: {e}")

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    try:
        data = json.loads(body)
        loan_id = data.get('loan_id')
        if loan_id:
            generate_pdf(loan_id)
    except Exception as e:
        print(f" [!] Error processing message: {e}")

def start_consuming():
    # Retry connection logic for Docker startup
    retries = 5
    while retries > 0:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='document_generation')
            
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.basic_consume(queue='document_generation', on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
            break
        except pika.exceptions.AMQPConnectionError:
            print(f" [!] RabbitMQ not ready, retrying in 5s... ({retries} left)")
            time.sleep(5)
            retries -= 1
    
    if retries == 0:
        print(" [!] Could not connect to RabbitMQ")

if __name__ == '__main__':
    start_consuming()
