from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import random
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Partner, Client, Card, Batch
from .forms import PartnerForm
import datetime
from django.conf import settings
import os
from fpdf import FPDF
import qrcode

# Create your views here.
def index(request):
    return render(request, 'index.html')

def partners(request):
    return render(request, 'partners.html')

def validatepage(request, cdno):
    
    try:
        test = Card.objects.get(cardno = cdno.strip())
        # return HttpResponse("Hurray found card!")
        
        dcco = {
            'validity':1,
            'test' : test,
            'cardno' : cdno,
        }
        return render(request, 'paypage.html', dcco)
    except Card.DoesNotExist:
        # return HttpResponse("Card does not exist!")
        dcco = {
            'validity' : 0,
            'cardno' : cdno,
        }
        return render(request, 'paypage.html', dcco)


def confam(request):
    if request.method == 'POST':
        card = request.POST['txtcard']
        return redirect(validatepage, card.strip())
        

    
    

    return render(request, 'confirm.html')

def loginuser(request):
    dicta = {}
    thd = 'Welcome'
    mtag = 'success'
    uname = request.POST['txtusername']
    pword = request.POST['txtpassword']
    
    user = authenticate(username=uname, password=pword)
    if user is not None:
        login(request, user)
        messages.success(request, f"Welcome {uname}")
        
    else:
        mtag = 'error'
        messages.error(request, "Your Login attempt is unsuccessful!", {'ercode':'info'})
    
    dicta = {
        'tHeading':thd,
        'tTage':mtag,

    }
        
    return render (request, 'index.html', dicta)

def loogout(request):
    logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('roothome')
    
def mnpartners(request):
    thd = 'Partner'
    mtag = 'success'

    fpartner = PartnerForm()

    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save()
            mtag = 'success'
            messages.success(request, 'New partner created successfully!')
        else:
            mtag = 'error'
            messages.error(request, 'Partner creation failed!')
    
    
    ptnr = Partner.objects.all()
    return render(request, 'crpartners.html', {'partners':ptnr, 'form':fpartner, 'tHeading':thd, 'tTag':mtag})


def mnclients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients':clients})

def clientana(request, id):
    client = get_object_or_404(Client, pk=id)
    ass_batch = client.batches.filter(printed = 0)

    tot = client.cards.all().count()
    red = client.cards.filter(status = 1).count()
    blk = client.cards.filter(status = 2).count()
    bal = client.cards.filter(status = 0).count()

    # creating batches
    # max_batch = 3000
    # i = 1
    # while i <= max_batch:
    #     try:
    #         letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #         lumpa = list(range (10000, 100000))
    #         batc = random.choice(list(letters)) + str(random.choice(list(lumpa)))
    #         tt = Batch.objects.create(batchno = batc)
    #         tt.save()
    #         i = i + 1
    #     except:
    #         pass

    if request.method == 'POST':
        batches = int(request.POST['selbatches'])
        e = 0
        batchlist = []
        while e < batches:
            try:
                # select a batchno
                bat = random.choice(Batch.objects.filter(status = 0))
                batchlist.append(bat.batchno)
                e = e + 1
            except:
                pass

        
        
        for bb in batchlist:
            id_batch = Batch.objects.get(batchno = bb).id
            c = 0

            # 500 is the number of card in a batch
            while c < 500:
                new_card = str(random.choice(list(range(100,999)))) + str(random.choice(list(range(1000,9999)))) + "-" + bb + "-" + str(random.choice(list(range(100,999)))) + str(datetime.datetime.now())[-6:]
                c = c + 1
                # print(new_card)
                crd =  Card.objects.create(batchno_id = id_batch, cardno = new_card, client_id = id)
                crd.save()
            
            batchfix = get_object_or_404(Batch, batchno = bb)
            batchfix.status = 1
            batchfix.client_id = id
            batchfix.save()

        return redirect(clientana, id)


    ddc = {
        'client':client,
        'tot_card':tot,
        'blocked_cards':blk,
        'redeemed':red,
        'free_cards':bal,
        'batches': ass_batch,
    }

    return render(request, 'clientdetail.html', ddc)

def batchview(request, batch):
    tg = get_object_or_404(Batch, pk = batch)
    cards = Card.objects.filter(batchno = batch)
    stat_free = Card.objects.filter(batchno = batch, status = 0).count()
    stat_red = Card.objects.filter(batchno = batch, status = 1).count()
    stat_blocked = Card.objects.filter(batchno = batch, status = 2).count()


    dic = {
        'target':tg,
        'cards':cards,
        'stat_free':stat_free,
        'stat_red':stat_red,
        'stat_blocked':stat_blocked,
    }
    return render(request, 'batchview.html', dic)

def card_tempa(request, id):
    deta = get_object_or_404(Card, pk = id)
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'BU', 12)
    # title must always follow below here
    pdf.cell(0, 7, "SINGLE CARD TEMPLATE", align="C")
    pdf.ln(30)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 7, 'Batch No:', align="L", border=0)
    top_y = pdf.get_y()-3
    pdf.set_font('Arial', '', 12)
    pdf.cell(120, 7, f'{str(deta.batchno)}', align="L", border=0)
    pdf.ln(8)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 7, 'Card Number:', align="L", border=0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(120, 7, deta.cardno, align="L", border=0)
    pdf.ln(8)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 7, 'Sponsor:', align="L", border=0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(120, 7, f'{str(deta.client)}', align="L", border=0)
    pdf.line(10, pdf.get_y() + 8, 200, pdf.get_y() + 8)

    data = str(deta.cardno)
    datax = "www.google.com/" + data # to be modified later and used in the line below instead of data
    img = qrcode.make(data)
    img_name = deta.cardno + '.png'
    img_name = settings.MEDIA_ROOT + '/' + img_name
    img.save(img_name)
    pdf.image(img_name, 175, top_y, 25, 25)
    if os.path.exists(img_name):
        os.remove(img_name)

    pdf.output('giftcard.pdf', 'I')
    return FileResponse(open('giftcard.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

def card_tempb(request, bat):
    targs = Card.objects.filter(batchno = bat, status = 0)
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'BU', 12)
    # title must always follow below here
    pdf.cell(0, 7, "BATCH CARD TEMPLATES", align="C")
    pdf.ln(10)
    lp = 0
    for tt in targs:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 7, 'Batch No:', align="L", border=0)
        top_y = pdf.get_y()
        pdf.set_font('Arial', '', 12)
        pdf.cell(120, 7, f'{str(tt.batchno)}', align="L", border=0)
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 7, 'Card Number:', align="L", border=0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(120, 7, tt.cardno, align="L", border=0)
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 7, 'Sponsor:', align="L", border=0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(120, 7, f'{str(tt.client)}', align="L", border=0)
        pdf.line(10, pdf.get_y() + 8, 200, pdf.get_y() + 8)
        pdf.ln(10)

        data = str(tt.cardno)
        datax = "www.google.com/" + data # to be modified later and used in the line below instead of data
        img = qrcode.make(data)
        img_name = tt.cardno + '.png'
        img_name = settings.MEDIA_ROOT + '/' + img_name
        img.save(img_name)
        pdf.image(img_name, 175, top_y, 20, 20)
        if os.path.exists(img_name):
            os.remove(img_name)
        
        lp = lp + 1
        if lp == 9:
            lp = 0
            pdf.add_page()
            pdf.set_font('Arial', 'BU', 12)
            pdf.cell(0, 7, "BATCH CARD TEMPLATES", align="C")
            pdf.ln(10)
            

    pdf.output('giftcards.pdf', 'I')
    return FileResponse(open('giftcards.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


def block_batch(request, bat):
    cardd = Card.objects.filter(batchno = bat, status = 0)
    
    try:
        for cd in cardd:
            cd.status = 2
            cd.save()
    except:
        pass

    return redirect(batchview, bat)

def contact(request):
    return render(request, 'contact.html')














class FPDF(FPDF):
    def header(self):
        # self.image("static/img/mymy.jpg", 0, 3, 35, 35)
        # self.image("static/img/backy.jpg", 50, 90, 120, 120)
        self.set_font('Arial', 'BU', 18)
        self.cell(0,8, "GIFTCARD TEMPLATES", align="C")
        self.ln(7)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 11)
        pageNum = self.page_no()
        self.cell(0,15, str(pageNum), align="R")