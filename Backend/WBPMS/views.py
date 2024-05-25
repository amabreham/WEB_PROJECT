
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import *

from telnetlib import STATUS
from urllib import request
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def login(request):
     
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        cust = Customer.objects.filter(Username=username,Password=password).exists()

        if user:
            auth.login(request,user)
            return redirect('/')
        elif cust:
            auth.login(request,cust)
            return redirect('/')
       
        else:
            messages.info(request, "Invalid Credential!")
            return render(request,"login.html", {'username':username})

        
    else:     
        return render(request,"login.html")
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    
def logout(request):
    auth.logout(request)
    return redirect('/') 
 

def index(request):
    notify_msg = Message.objects.filter(recv_name=request.user.username)
    notify_msg = notify_msg.filter(status='unread').all()
    notification = notify_msg.count()
    drug = Medicine.objects.filter(Category='Cosmotics')
    return render(request, 'home.html', {'drug':drug, 'notice':notification})


def customerReg(request):
    if request.method == 'POST':
        Username = request.POST['username']
        Email = request.POST['email']
        Password = request.POST.get('password')
        Confpass = request.POST.get('password1')
        customer = request.POST.get('customer')

        context = {'username':Username, 'email':Email}
        
        
        if User.objects.filter(username=Username).exists():
            messages.info(request, "Username already exists")
            return render(request, 'cust_register.html', context)


        else:
            if Password.__len__() > 5:
                if Password == Confpass:
                    Password = make_password(Password)
                    # Customer.objects.create(Username=Username, Email=Email,Password=Password).save()

                    User.objects.create(username=Username, email=Email,password=Password).save()
                    Profile.objects.create(user=User.objects.get(username=Username), position=customer).save()
                    return redirect('login')
                else:
                    messages.info(request, "Password does't match")
                    return render(request, 'cust_register.html', context)
            else:
                messages.info(request, "Password is too short")
                return render(request, 'cust_register.html', context)
          
                          
    else:
       return render(request, 'cust_register.html')                  
    
####drug update##########

def add_drug(request):
   if request.user.is_authenticated:
         
        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notification = notify_msg.count()
        return render(request, 'add_drug.html', {'notice':notification})
       
          
   else:
       return redirect('login')
  

    ##### product list #####
def productList(request):
    notify_msg = Message.objects.filter(recv_name=request.user.username)
    notify_msg = notify_msg.filter(status='unread').all()
    notification = notify_msg.count()
    product = JemoMedicine.objects.all()
    return render(request, 'product.html', {'product':product, 'notice':notification})
    ###aboutUs ###


def aboutUs(request):
    notify_msg = Message.objects.filter(recv_name=request.user.username)
    notify_msg = notify_msg.filter(status='unread').all()
    notification = notify_msg.count()
    return render(request, 'about.html', {'notice':notification})    

def contactus(request):

    return render(request, 'contactUs.html') 
   

    #########Adding Medicine########

def manageDrug(request):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist') or (request.user.is_authenticated and request.user.profile.position == 'Pharmacist'):
        # 

        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notification = notify_msg.count()
        viewdrug = Medicine.objects.all()
        import datetime
        for v in viewdrug:
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
            v.Days = days
            v.Expired_Date = left_time
        if request.method == "POST":
            medicineName = request.POST['name']
            batchNumber = request.POST['batchno']
            medicineImage = request.FILES.get('medimage')
            category = request.POST['category']
            expiredDate = request.POST['expireddate']
            price = request.POST['price']
            description = request.POST['description']
            branch = request.POST.get('branch')
            quantity = request.POST['quantity']


        
            if medicineName=="" or batchNumber=="" or medicineImage=="" or category=="" or expiredDate=="" or price=="" or description=="":  
                messages.info(request, "Please fill all fields")   
                return render(request, 'manageDrug.html', {'views':viewdrug})
            else:
                medicineName = medicineName.lower()
                adding = Medicine.objects.create(Name=medicineName, Batch_Number=batchNumber, Image=medicineImage,
                        Category=category,Expired_Date=expiredDate, Unit_Price=price, Description=description, Branch=branch,Quantity=quantity)
                adding.save()
                messages.info(request, "Success!!")   

            return render(request, 'manageDrug.html', {'notice':notification, 'views':viewdrug})
        else:
            return render(request, 'manageDrug.html', {'notice':notification, 'views':viewdrug})


    else:
       return redirect('login')

from django.utils.dateparse import parse_date
def viewDrugs(request):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist') or (request.user.is_authenticated and request.user.profile.position == 'Pharmacist'):
        import datetime
        view_branch_drug = Medicine.objects.all().order_by('Name')
        for v in view_branch_drug:
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
                exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                exdates = exdates.days
            v.exdate = exdates
            v.Days = days
            v.Expired_Date = left_time
        left_time = 0

        drug_lebu = LebuMedicine.objects.all().count()
        drug_jemo = JemoMedicine.objects.all().count()
        drug_main = Medicine.objects.all().count()
 
        type_cosmotics = Medicine.objects.filter(Category='Cosmotics').count()
        type_GIT = Medicine.objects.filter(Category='GIT').count()
        type_CNS = Medicine.objects.filter(Category='CNS').count()
        type_ENT= Medicine.objects.filter(Category='ENT').count()
        type_CVS = Medicine.objects.filter(Category='CVS').count()
        type_Minerals = Medicine.objects.filter(Category='Minerals').count()
        type_Hormones = Medicine.objects.filter(Category='Hormones').count()
        type_Anti_virals = Medicine.objects.filter(Category='Anti_virals').count()
        type_Anti_infectives = Medicine.objects.filter(Category='Anti_infectives').count()
        type_Anti_helmentics = Medicine.objects.filter(Category='Anti_helmentics').count()
        type_Maskuloskeletal = Medicine.objects.filter(Category='Maskuloskeletal').count()
        type_Medical_Supplies = Medicine.objects.filter(Category='Medical_Supplies').count()
        
        
        if 'expired' in request.POST:
            id = request.POST.get('medID')
            name = request.POST['name']
            batch = request.POST['batchno']
            quantity = request.POST['quantity']
            category = request.POST['category']
            price = request.POST['price']
            branch = request.POST.get('branch')

            
            if name!="" and batch!="" and category!="" and price!="":
                checking = ExpiredDrug.objects.filter(Name=name,branch=branch, Unit_Price=price).all()

                if checking:
                    for check in checking:
                            quan = check.Quantity + int(quantity)
                            tprice = quan * check.Unit_Price
                            ExpiredDrug.objects.filter(Name=name,branch=branch, Unit_Price=price).update(Quantity=quan, Total=tprice)
                            Medicine.objects.filter(pk=id).delete()

                else:
  
                    ExpiredDrug.objects.create(Name=name, Batch_Number=batch, Category=category,
                            Unit_Price=price, branch=branch).save()
                    Medicine.objects.filter(pk=id).delete()
                    viewdrug = Medicine.objects.all()
                    num = viewdrug.count()
                    context = {'views':viewdrug, 'num':num,  'view_branch_drug':view_branch_drug}

                    return render(request, 'view-drug.html', context)
            else:
                viewdrug = Medicine.objects.all()
                num = Medicine.objects.all().count()
                context = {'views':viewdrug, 'num':num,  'view_branch_drug':view_branch_drug}
                return render(request, 'view-drug.html', context)   

        
        
        if 'add' in request.POST:
            medicineName = request.POST['name']
            batchNumber = request.POST['batchno']
            medicineImage = request.FILES.get('medimage')
            category = request.POST['category']
            expiredDate = request.POST['expireddate']
            price = request.POST['price']
            description = request.POST['description']
            branch = request.POST.get('branch')
            quantity = request.POST.get('quantity')

            success = "success"    
            context = {'name':medicineName, 'batch':batchNumber, 'category':category, 'date':expiredDate, 'price':price, 'desc':description, 'quantity':quantity, 'view_branch_drug':view_branch_drug}
            date_str = request.POST.get('expireddate')
            exdate = parse_date(date_str)
            exdate = int(exdate.strftime('%Y%m%d'))
            date = datetime.datetime.now()
            date = int(date.strftime('%Y%m%d'))
    
            if int(exdate) < date:
                messages.info(request, "enter correct date")
                return render(request, 'add_druginMainBranch.html', {'view_branch_drug':view_branch_drug})
            else:
                medicineName = medicineName.lower()
                adding = Medicine.objects.create(Name=medicineName, Batch_Number=batchNumber, Image=medicineImage,
                        Category=category,Expired_Date=expiredDate, Unit_Price=price, Description=description,
                        Branch=branch, Quantity=quantity)
                adding.save()
                messages.info(request, "Successfully added!!")   
                return render(request, 'add_druginMainBranch.html', {"success":success, 'view_branch_drug':view_branch_drug})
           
 
 
        if 'J_modify' in request.POST:
            jemo_branch = Medicine.objects.filter(Branch='Head Office').all()

            drug_id = request.POST.get('drug_id')
            drug_name = request.POST.get('drug_name')
            avail_branch = request.POST.get('avail_branch')
            drug_branch = request.POST.get('drug_branch')
            drug_price = request.POST.get('drug_price')
            avail_quantity = request.POST.get('avail_quantity')
            sell_quantity = request.POST.get('sell_quantity')
            category = request.POST.get('category')
            ex_date = request.POST.get('ex_date')

            if sell_quantity is None or sell_quantity == "" or sell_quantity == 0:
                context = {"jemo_branch": jemo_branch}
                return render(request, "add_druginJemo.html", context)
            else:
            # branch_drug = Medicine.objects.filter(pk=drug_id)
                if Medicine.objects.filter(pk=drug_id) and int(avail_quantity) == int(sell_quantity):
                    branch_drug = Medicine.objects.filter(pk=drug_id)
                    for branch_drug in branch_drug:

                        JemoMedicine.objects.create(Name=drug_name, Batch_Number=branch_drug.Batch_Number, Image=branch_drug.Image,
                                        Category=branch_drug.Category,Expired_Date=branch_drug.Expired_Date, Selector=branch_drug.pk, Unit_Price=drug_price, Description=branch_drug.Description,
                                            Branch=drug_branch, Quantity=sell_quantity).save()
                        Medicine.objects.filter(pk=drug_id).delete()
                        messages.info(request, "Seccessfully added")
                        context = {"jemo_branch": jemo_branch}

                        messages.info(request, "Success")
                        return render(request, "add_druginJemo.html", context)
                else:
                    if int(avail_quantity) < int(sell_quantity):
                        context = {"jemo_branch": jemo_branch}

                        messages.info(request, "quantity to be sold should be <= available quantity")
                        return render(request, "add_druginJemo.html", context)
                    
                    else: 
                        branch_drug = Medicine.objects.filter(pk=drug_id)

                        tobeadd = JemoMedicine.objects.filter(Selector=drug_id)
                        if tobeadd:
                            for tobeadd in tobeadd: 
                                quantity = tobeadd.Quantity + int(sell_quantity)
                                JemoMedicine.objects.filter(Selector=drug_id).update(Quantity=quantity)
                            for branch_drug in branch_drug:
                                quantity = branch_drug.Quantity -  int(sell_quantity) 
                                Medicine.objects.filter(pk=drug_id).update(Quantity=quantity)
                            context = {"jemo_branch": jemo_branch}

                            messages.info(request, "Seccessfully added")
                            return render(request, "add_druginJemo.html", context)
                        else:
                            for branch_drug in branch_drug:
                                JemoMedicine.objects.create(Name=drug_name, Batch_Number=branch_drug.Batch_Number, Image=branch_drug.Image,
                                    Category=branch_drug.Category,Expired_Date=branch_drug.Expired_Date, Selector=branch_drug.pk, Unit_Price=drug_price, Description=branch_drug.Description,
                                        Branch=drug_branch, Quantity=sell_quantity).save()
                                quantity = branch_drug.Quantity -  int(sell_quantity) 
                                Medicine.objects.filter(pk=drug_id).update(Quantity=quantity)
                            messages.info(request, "Seccessfully added")
                            context = {"jemo_branch": jemo_branch}

                            return render(request, "add_druginJemo.html", context)
                        
        if 'L_modify' in request.POST:
            lebu_branch = Medicine.objects.all()

            drug_id = request.POST.get('drug_id')
            drug_name = request.POST.get('drug_name')
            avail_branch = request.POST.get('avail_branch')
            drug_branch = request.POST.get('drug_branch')
            drug_price = request.POST.get('drug_price')
            avail_quantity = request.POST.get('avail_quantity')
            sell_quantity = request.POST.get('sell_quantity')

            if sell_quantity is None or sell_quantity == "" or sell_quantity == 0:
                context = {"lebu_branch": lebu_branch}
                return render(request, "add_druginLebu.html", context)
            else:
            # branch_drug = Medicine.objects.filter(pk=drug_id)
                if Medicine.objects.filter(pk=drug_id) and int(avail_quantity) == int(sell_quantity):
                    branch_drug = Medicine.objects.filter(pk=drug_id)
                    for branch_drug in branch_drug:

                        LebuMedicine.objects.create(Name=drug_name, Batch_Number=branch_drug.Batch_Number, Image=branch_drug.Image,
                                        Category=branch_drug.Category,Expired_Date=branch_drug.Expired_Date, Selector=branch_drug.pk, Unit_Price=drug_price, Description=branch_drug.Description,
                                            Branch=drug_branch, Quantity=sell_quantity).save()
                        Medicine.objects.filter(pk=drug_id).delete()
                        messages.info(request, "Seccessfully added")
                        context = {"lebu_branch": lebu_branch}
        
                        messages.info(request, "Success")
                        return render(request, "add_druginLebu.html", context)
                else:
                    if int(avail_quantity) < int(sell_quantity):
                        context = {"lebu_branch": lebu_branch}

                        messages.info(request, "quantity to be sold should be <= available quantity")
                        return render(request, "add_druginLebu.html", context)
                    
                    else: 
                        branch_drug = Medicine.objects.filter(pk=drug_id)

                        tobeadd = LebuMedicine.objects.filter(Selector=drug_id)
                        if tobeadd:
                            for tobeadd in tobeadd: 
                                quantity = tobeadd.Quantity + int(sell_quantity)
                                LebuMedicine.objects.filter(Selector=drug_id).update(Quantity=quantity)
                            for branch_drug in branch_drug:
                                quantity = branch_drug.Quantity -  int(sell_quantity) 
                                Medicine.objects.filter(pk=drug_id).update(Quantity=quantity)
                            context = {"lebu_branch": lebu_branch}

                            messages.info(request, "Seccessfully added")
                            return render(request, "add_druginLebu.html", context)
                        else:
                            for branch_drug in branch_drug:
                                LebuMedicine.objects.create(Name=drug_name, Batch_Number=branch_drug.Batch_Number, Image=branch_drug.Image,
                                    Category=branch_drug.Category,Expired_Date=branch_drug.Expired_Date, Selector=branch_drug.pk, Unit_Price=drug_price, Description=branch_drug.Description,
                                        Branch=drug_branch, Quantity=sell_quantity).save()
                                quantity = branch_drug.Quantity -  int(sell_quantity) 
                                Medicine.objects.filter(pk=drug_id).update(Quantity=quantity)
                            messages.info(request, "Seccessfully added")
                            context = {"lebu_branch": lebu_branch}

                            return render(request, "add_druginLebu.html", context)
            
            
        
            
        if 'update' in request.POST:
             
            medicineName = request.POST['name']
            batchNumber = request.POST['batchno']
            medicineImage = request.FILES.get('medimage')
            category = request.POST.get('category')
            expiredDate = request.POST.get('expireddate')
            price = request.POST.get('price')
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')

            
            medicineID = request.POST.get('medID')
            update_drug = Medicine.objects.filter(pk=medicineID)
            success = "success"
            if update_drug: 
                if medicineImage:
                    update_drug.update(Name=medicineName,Image=medicineImage,Batch_Number=batchNumber,
                            Category=category,Expired_Date=expiredDate,Unit_Price=price,
                            Description=description, Quantity = quantity)
                    messages.info(request, "Successfully updated")
                    return render(request, 'manageDrug.html', {"success":success ,'views':viewdrug, 'view_branch_drug':view_branch_drug})   
                else:
                    update_drug.update(Name=medicineName, Batch_Number=batchNumber,
                            Category=category,Expired_Date=expiredDate,Unit_Price=price,
                            Description=description,Quantity=quantity)
                    messages.info(request, "Successfully updated")
                    return render(request, 'manageDrug.html', {"success":success, 'view_branch_drug':view_branch_drug})   
            else: 
                messages.info(request, "Error updating")
                return render(request, 'manageDrug.html', {'view_branch_drug':view_branch_drug})  

        if 'L_update' in request.POST:
             
            medicineName = request.POST['name']
            batchNumber = request.POST['batchno']
            medicineImage = request.FILES.get('medimage')
            category = request.POST.get('category')
            expiredDate = request.POST.get('expireddate')
            price = request.POST.get('price')
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')

            
            medicineID = request.POST.get('medID')
            update_drug = LebuMedicine.objects.filter(pk=medicineID)
            success = "success"
            if update_drug: 
                if medicineImage:
                    update_drug.update(Name=medicineName,Image=medicineImage,Batch_Number=batchNumber,
                            Category=category,Expired_Date=expiredDate,Unit_Price=price,
                            Description=description, Quantity = quantity)
                    messages.info(request, "Successfully updated")
                    return render(request, 'L_updating.html', {"success":success ,'views':viewdrug, 'view_branch_drug':view_branch_drug})   
                else:
                    update_drug.update(Name=medicineName, Batch_Number=batchNumber,
                            Category=category,Expired_Date=expiredDate,Unit_Price=price,
                            Description=description,Quantity=quantity)
                    messages.info(request, "Successfully updated")
                    return render(request, 'L_updating.html', {"success":success, 'view_branch_drug':view_branch_drug})   
            else: 
                messages.info(request, "Error updating")
                return render(request, 'L_updating.html', {'view_branch_drug':view_branch_drug})  


        if 'J_update' in request.POST:
             
            medicineName = request.POST['name']
            batchNumber = request.POST['batchno']
            medicineImage = request.FILES.get('medimage')
            category = request.POST.get('category')
            expiredDate = request.POST.get('expireddate')
            price = request.POST.get('price')
            description = request.POST.get('description')
            quantity = request.POST.get('quantity')

            
            medicineID = request.POST.get('medID')
            update_drug = JemoMedicine.objects.filter(pk=medicineID)
            success = "success"
            if update_drug: 
                if medicineImage:
                    update_drug.update(Name=medicineName,Image=medicineImage,Batch_Number=batchNumber,
                            Category=category,Expired_Date=expiredDate,Unit_Price=price,
                            Description=description, Quantity = quantity)
                    messages.info(request, "Successfully updated")
                    return render(request, 'J_updating.html', {"success":success ,'views':viewdrug, 'view_branch_drug':view_branch_drug})   
                else:
                    update_drug.update(Name=medicineName, Batch_Number=batchNumber,
                            Category=category,Expired_Date=expiredDate,Unit_Price=price,
                            Description=description,Quantity=quantity)
                    messages.info(request, "Successfully updated")
                    return render(request, 'J_updating.html', {"success":success, 'view_branch_drug':view_branch_drug})   
            else: 
                messages.info(request, "Error updating")
                return render(request, 'J_updating.html', {'view_branch_drug':view_branch_drug})  




        if 'delete' in request.POST:
            drug_jemo = Medicine.objects.filter(Branch="Jemo").all().count()
            medicineID = request.POST.get('medID')
            update_drug = Medicine.objects.all().filter(pk=medicineID)
            if update_drug:
                update_drug.delete()
                messages.info(request, "Successfully deleted")
                return render(request, 'view-drug.html', {'view_branch_drug':view_branch_drug}) 
            else:
                return render(request, 'view-drug.html') 
        import datetime
        viewdrug = Medicine.objects.all()
        for v in viewdrug:
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
                exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                exdates = exdates.days
            v.exdate = exdates
            v.Days = days
            v.Expired_Date = left_time

        
        context = {'view_branch_drug':view_branch_drug, 'drug_main':drug_main, 'drug_lebu':drug_lebu, 'drug_jemo':drug_jemo,'left_time':left_time, 'views':viewdrug, 'minerals':type_Minerals, 
                'cosmotics':type_cosmotics, 'GIT':type_GIT, 'CNS':type_CNS,'ENT':type_ENT,
                'CVS':type_CVS, 'hormones':type_Hormones, 'Anti_virals':type_Anti_virals, 
                'Anti_infectives':type_Anti_infectives, 'Anti_helmentics':type_Anti_helmentics,
                'maskuloskeletal':type_Maskuloskeletal, 'Medical_Supplies':type_Medical_Supplies}
        return render(request, 'view-drug.html', context)

    else:
        return redirect('login')


def viewDrug(request, id):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist') or (request.user.is_authenticated and request.user.profile.position == 'Pharmacist'):
        search = Medicine.objects.filter(pk=id).all()
           
        left_time = 0
        notify_msg = Message.objects.filter(recv_name=request.user.username).all()
        notify_msg = notify_msg.filter(status='unread').all()
        notificate = notify_msg.count()
       
         
        # viewdrug = Medicine.objects.filter(Branch=request.user.profile.branch)
       

        context = {'search':search }
        return render(request, 'manageDrug.html', context)

    else:
        return redirect('login')

def L_update(request, id):
     if (request.user.is_authenticated and request.user.profile.position == 'Druggist') or (request.user.is_authenticated and request.user.profile.position == 'Pharmacist'):
         L_search = LebuMedicine.objects.filter(pk=id).all()
         context = {'L_search':L_search }
         return render(request, 'L_updating.html', context)
     else:
        return redirect('login')
     
def J_update(request, id):
     if (request.user.is_authenticated and request.user.profile.position == 'Druggist') or (request.user.is_authenticated and request.user.profile.position == 'Pharmacist'):
         J_search = JemoMedicine.objects.filter(pk=id).all()
         context = {'J_search':J_search }
         return render(request, 'J_updating.html', context)
     else:
        return redirect('login')
def category(request):
    notify_msg = Message.objects.filter(recv_name=request.user.username).all()
    notify_msg = notify_msg.filter(status='unread').all()
    notificate = notify_msg.count()
    Cosmotics = Medicine.objects.filter(Category='Cosmotics')
    GITs = Medicine.objects.filter(Category='GIT')
    CNSs = Medicine.objects.filter(Category='CNS')
    ENTs= Medicine.objects.filter(Category='ENT')
    CVSs = Medicine.objects.filter(Category='CVS')
    Minerals = Medicine.objects.filter(Category='Minerals')
    Hormones = Medicine.objects.filter(Category='Hormones')
    Anti_virals = Medicine.objects.filter(Category='Anti_virals')
    Anti_infectives = Medicine.objects.filter(Category='Anti_infectives')
    Anti_helmentics = Medicine.objects.filter(Category='Anti_helmentics')
    Maskuloskeletal = Medicine.objects.filter(Category='Maskuloskeletal')
    Medical_Supplies = Medicine.objects.filter(Category='Medical_Supplies')
    if Cosmotics or GITs or CNSs or ENTs or CVSs or Minerals or Hormones or Anti_virals or Anti_infectives or Anti_helmentics or Maskuloskeletal or Medical_Supplies :
        return render(request, "category.html", {'Cosmotics':Cosmotics, 'GIT':GITs, 'CNS':CNSs, 'ENT':ENTs, 'CVS':CVSs, 'Minerals':Minerals, 'Hormones':Hormones,
                         'Anti_virals':Anti_virals, 'Anti_infectives':Anti_infectives, 'Anti_helmentics':Anti_helmentics, 'Maskuloskeletal':Maskuloskeletal,
                         'Medical_Supplies':Medical_Supplies, 'notice':notificate})



    ############## Search drug ############
def search(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search!="":
            search = search.lower()
            drugs = Medicine.objects.all().filter(Name=search)
            
            if drugs:
               drug_name = search
               return render(request, 'search.html', {'drugs':drugs, 'drug_name':drug_name})
            else:
                drug_name = search
                messages.info(request, "Drug not found try again")
                context = {'drug_name':drug_name}
                return render(request, 'search.html', context)
        else:
            return redirect("index")
#### chating #####
def response(request):
    notify_msg = Message.objects.filter(recv_name=request.user.username)
    notify_msg = notify_msg.filter(status='unread').all()
    notification = notify_msg.count()
    response = Response.objects.all()   
    return render(request, "response.html", {'user':response, 'notices':notification})

def advice(request, pk):
    if (request.user.is_authenticated and request.user.profile.position == 'Pharmacist') or (request.user.is_authenticated and request.user.profile.position == 'Customer'):
        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notification = notify_msg.count()
        custom  = User.objects.get(pk=pk)
        sent_msg = Message.objects.all()
        customer = User.objects.all()
        sender = ""
        message=""
        id = ""
        reciever = ""
        for sentmsg in sent_msg:
            if sentmsg.recv_name == request.user.username or sentmsg.send_name == request.user.username:
                message = sentmsg.msg
                sender = sentmsg.send_name
                reciever = sentmsg.recv_name

                id = sentmsg.pk
            id = id
            id = id

        context = {'custom':custom, 'msg':sent_msg, 'customer':customer, 'notice':notification,
                'message':message, 'sender':sender, 'id':id, 'reciever':reciever}
    
        if request.method == "POST":
                sender = request.POST.get('msg_sender')
                reciever = request.POST.get('msg_reciever')
                message = request.POST.get('message') 
                if sender is None or reciever is None or message is None:  
                    return redirect('advice')
                else:
                    if message!="":
                        

                        Message.objects.create(send_name=sender, recv_name=reciever,
                                    msg=message).save()
                        message = ""
                        sent_msg = Message.objects.all()
                        customer = User.objects.all()

                        context = {'msg':sent_msg, 'message':message, 'custom':custom, 'customer':customer}
                        return render(request, "chatt.html",context)   
                    
                sent_msg = Message.objects.all()
                customer = User.objects.all()

                context = {'msg':sent_msg, 'message':message, 'custom':custom, 'customer':customer}
                return render(request, "chatt.html", context)     
    
        else:
            return render(request, "chatt.html",context)  
    else:
        return redirect('login')

def chat(request):   
    
    if (request.user.is_authenticated and request.user.profile.position == 'Pharmacist') or (request.user.is_authenticated and request.user.profile.position == 'Customer'):

        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notification = notify_msg.count()
        customer = User.objects.all()
        sent_msg = Message.objects.all()
        sender = ""
        message=""
        id = ""
        reciever = ""
        for sentmsg in sent_msg:
            if sentmsg.recv_name == request.user.username or sentmsg.send_name == request.user.username:
                message = sentmsg.msg
                sender = sentmsg.send_name
                reciever = sentmsg.recv_name

                id = sentmsg.pk
            
        context = {'customer':customer, 'notice':notification, 'msg':sent_msg, 
                   'message':message, 'sender':sender, 'id':id, 'reciever':reciever}
        return render(request, "chatt.html",context)
        
    else:
        return redirect('login')

def chat_delete(request):   
    
    if (request.user.is_authenticated and request.user.profile.position == 'Pharmacist') or (request.user.is_authenticated and request.user.profile.position == 'Customer'):

        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notification = notify_msg.count()
        customer = User.objects.all()
        sent_msg = Message.objects.all()
        sender = ""
        message=""
        id = ""
        reciever = ""
        for sentmsg in sent_msg:
            if sentmsg.recv_name == request.user.username or sentmsg.send_name == request.user.username:
                message = sentmsg.msg
                sender = sentmsg.send_name
                reciever = sentmsg.recv_name

                id = sentmsg.pk
        context = {'customer':customer, 'notice':notification, 'msg':sent_msg, 
                   'message':message, 'sender':sender, 'id':id, 'reciever':reciever}
        if request.method == "POST":
            sname = request.POST.get('sname')
            delete_msg1 = Message.objects.filter(send_name=sname,recv_name=request.user.username )
            delete_msg2 = Message.objects.filter(send_name=request.user.username, recv_name=sname)
            if delete_msg1 or delete_msg2:
                delete_msg2.delete()
                delete_msg1.delete()
                return render(request, "chatt.html",context)

       
        return render(request, "chatt.html",context)
        
    else:
        return redirect('login')    
    

def notification(request):
    if request.user.is_authenticated:
        notify_msg = Message.objects.filter(recv_name=request.user.username).all()
        notify_msg = notify_msg.filter(status='unread').all()
        notificate = notify_msg.count()
 
        notify_msg = Message.objects.filter(recv_name=request.user.username).all()
        # if notificate:
        if notify_msg:
            for notify in notify_msg:
                if notify.status == 'unread':
                    notify_msg.all().update(status='read')
        customer = User.objects.all()
        sent_msg = Message.objects.all()
        sender = ""
        message=""
        id = ""
        reciever = "" 
        for sentmsg in sent_msg:
            if sentmsg.recv_name == request.user.username or sentmsg.send_name == request.user.username:
                message = sentmsg.msg
                sender = sentmsg.send_name
                reciever = sentmsg.recv_name

                id = sentmsg.pk
            
        context = {'customer':customer, 'msg':sent_msg, 
                   'message':message, 'sender':sender, 'id':id, 'reciever':reciever, 'notice':notificate}
        
        return render(request, "chatt.html", context)
            

    else:
        return redirect('login')
 

def J_CreateBill(request):
    
    if (request.user.is_authenticated and request.user.profile.position == 'Cashier'):
        
        left_time = 0
        import datetime
        if request.user.profile.branch == 'Jemo':
            bill =  JemoMedicine.objects.all().order_by('Name')
        if request.user.profile.branch == 'Lebu':
            bill =  LebuMedicine.objects.all().order_by('Name')
            
        for v in bill:
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
                exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                exdates = exdates.days
            v.exdate = exdates
            v.Days = days
            v.Expired_Date = left_time


        if 'adding' in request.POST: 
            
            drug_id = request.POST.get('drug_id')
            drug_name = request.POST.get('drug_name')
            drug_price = request.POST.get('drug_price')
            in_quantity = request.POST.get('in_quantity')
            out_quantity = request.POST.get('out_quantity')

            if in_quantity == 0 or in_quantity == "":
                # bill = Medicine.objects.all()
                temp = temp_bill.objects.all()
                tempbill = temp_bill.objects.all()
                grd_total = 0   
                for tempbill in tempbill:
                     grd_total += tempbill.total
                context = {'bill':bill, 'temp':temp, 'grd_total':grd_total}
                return render(request, "bill.html", context) 
            else:
                out_quantity = int(out_quantity)
                in_quantity = int(in_quantity)
                if out_quantity >= in_quantity: 
                    grd_total= 0
                    total = int(drug_price) * int(in_quantity)
                    temp_bill.objects.create(id=drug_id, name=drug_name, price=drug_price,Quant=in_quantity, total=total).save()
                    drug_name = ""
                    drug_price = ""
                    in_quantity = ""
                    tempbill = temp_bill.objects.all()
                    tempbill_count = tempbill.alast()
                    # bill = Medicine.objects.all()
                    for tempbill in tempbill:
                        grd_total += tempbill.total

                    temp = temp_bill.objects.all()
                    context = {'bill':bill, 'temp':temp, 'grd_total':grd_total, 'tempbill_count':tempbill_count}
                    return render(request, "bill.html", context)
                else:
                    temp = temp_bill.objects.all()
                    tempbill = temp_bill.objects.all()
                    grd_total = 0   
                    for tempbill in tempbill:
                        grd_total += tempbill.total
                    context = {'bill':bill, 'temp':temp, 'grd_total':grd_total, 'in_quantity':in_quantity, 'out_quantity':out_quantity}
                    messages.error(request,"you have left ")

                    return render(request, "bill.html", context)
            
        if 'remove' in request.POST:
            id = request.POST.get('med_id')
            temp_bill.objects.filter(pk=id).delete()
            tempbill = temp_bill.objects.all()
            # bill = Medicine.objects.all()
            temp = temp_bill.objects.all()
            

            grd_total = 0
            for tempbill in tempbill:
                     grd_total += tempbill.total
           
            context = {'bill':bill, 'temp':temp, 'grd_total':grd_total}
            return render(request, "bill.html", context)
        
        if 'clear' in request.POST:
                temp_bill.objects.all().delete()

            
        if 'print' in request.POST:
            id = request.POST.get('med_id')
            name = request.POST.get('med_name')
            creator = request.POST.get('creator')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            total = request.POST.get('total')
            branch = request.POST.get('branch')


            if name is not None and creator is not None and price is not None and quantity is not None:
                if request.user.profile.branch == 'Jemo':
                    quant = JemoMedicine.objects.filter(Name=name)
                    checking = Bill.objects.filter(medicine_name=name,Branch=branch)
                    if checking:
                        for check in checking:
                            for q in quant:
                                Bquantity = check.quantity + int(quantity)
                                Btotal = check.price * Bquantity
                                Juantity = q.Quantity - int(quantity)
                                Bill.objects.filter(medicine_name=name).update(quantity=Bquantity, total=Btotal)
                                JemoMedicine.objects.filter(Name=name).update(Quantity=Juantity)
                    else:
                        tempbill = temp_bill.objects.all()
                        for tempbill in tempbill:
                            Bill.objects.create(medicine_name=tempbill.name, user_name=creator, price=tempbill.price, 
                                    quantity=tempbill.Quant,total=tempbill.total, Branch=branch).save()
                            
                            med = JemoMedicine.objects.filter(id=tempbill.id)
                            for med in med:
                                med_quan = med.Quantity - tempbill.Quant 
                                if med_quan > 0:
                                    med.Quantity = med_quan
                                    JemoMedicine.objects.filter(id=tempbill.id).update(Quantity=med_quan)
                                    temp = temp_bill.objects.all()
                                    grd_total = 0
                                    for tempbill in temp:
                                        grd_total += tempbill.total
                                    context = {'bill':bill, 'temp':temp}
                                    return render(request, "bill.html", context)  
                                else:
                                    med.delete()
                                    temp = temp_bill.objects.all()
                                    context = {'bill':bill, 'temp':temp}
                                    return render(request, "bill.html", context)  

                if request.user.profile.branch == 'Lebu':
                    quant = LebuMedicine.objects.filter(Name=name)
                    checking = Bill.objects.filter(medicine_name=name,Branch=branch)
                    if checking:
                        for check in checking:
                            for q in quant:
                                Bquantity = check.quantity + int(quantity)
                                Btotal = check.price * Bquantity
                                Juantity = q.Quantity - int(quantity)
                                Bill.objects.filter(medicine_name=name).update(quantity=Bquantity, total=Btotal)
                                LebuMedicine.objects.filter(Name=name).update(Quantity=Juantity)
                    else:
                        tempbill = temp_bill.objects.all()
                        for tempbill in tempbill:
                            Bill.objects.create(medicine_name=tempbill.name, user_name=creator, price=tempbill.price, 
                                    quantity=tempbill.Quant,total=tempbill.total, Branch=branch).save()
                            
                            med = LebuMedicine.objects.filter(id=tempbill.id)
                            for med in med:
                                med_quan = med.Quantity - tempbill.Quant 
                                if med_quan > 0:
                                    med.Quantity = med_quan
                                    LebuMedicine.objects.filter(id=tempbill.id).update(Quantity=med_quan)
                                    temp = temp_bill.objects.all()
                                    grd_total = 0
                                    for tempbill in temp:
                                        grd_total += tempbill.total
                                    context = {'bill':bill, 'temp':temp}
                                    return render(request, "bill.html", context)  
                                else:
                                    med.delete()
                                    temp = temp_bill.objects.all()
                                    context = {'bill':bill, 'temp':temp}
                                    return render(request, "bill.html", context)  
                                
                        
                temp = temp_bill.objects.all()
                context = {'bill':bill, 'temp':temp}
                return render(request, "bill.html", context)
            else:
                context = {'bill':bill}
                return render(request, "bill.html", context)
        else:    
            grd_total= 0
            tempbill = temp_bill.objects.all()
            for tempbill in tempbill:
                    grd_total += tempbill.total
            
            temp = temp_bill.objects.all()
            context = {'bill':bill, 'temp':temp, 'grd_total':grd_total}
            return render(request, "bill.html", context)
     
    else:
        return redirect('login')
    
 
def sold_drug(request):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist') or request.user.is_authenticated and request.user.profile.position == 'Super Druggist':
        view_exp_drug = ExpiredDrug.objects.all().order_by('Date')
        import datetime

        price = 0
        for exp_price in view_exp_drug:
            exp_price.Total = exp_price.Unit_Price * exp_price.Quantity
            price += exp_price.Total
        sold_drug = Bill.objects.all().order_by('created_date')

        total = 0
        for exp_drug in sold_drug:
            total += exp_drug.total 
        
        for v in view_exp_drug:
            if v.Date:
                exdate = v.Date
                now = datetime.datetime.now()
                time_diff = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                time_diff = time_diff.days / 30
                time_diff = int(time_diff)
            v.time_diff = time_diff           
        context = {'sold_drug':sold_drug, 'total':total, 'exp_drug':view_exp_drug, 'price':price}
        return render(request,'drug_report.html', context)
    
    else:
        return redirect('login')


###### drugs in Branches  #####
def lebu_branch(request):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist'):
              
        medicine = LebuMedicine.objects.all().order_by('Name')
        total_num = medicine.count()

        Cosmotics = LebuMedicine.objects.filter(Category='Cosmotics').count()
        GITs = LebuMedicine.objects.filter(Category='GIT').count()
        CNSs = LebuMedicine.objects.filter(Category='CNS').count()
        ENTs= LebuMedicine.objects.filter(Category='ENT').count()
        CVSs = LebuMedicine.objects.filter(Category='CVS').count()
        Minerals = LebuMedicine.objects.filter(Category='Minerals').count()
        Hormones = LebuMedicine.objects.filter(Category='Hormones').count()
        Anti_virals = LebuMedicine.objects.filter(Category='Anti_virals').count()
        Anti_infectives = LebuMedicine.objects.filter(Category='Anti_infectives').count()
        Anti_helmentics = LebuMedicine.objects.filter(Category='Anti_helmentics').count()
        Maskuloskeletal = LebuMedicine.objects.filter(Category='Maskuloskeletal').count()
        Medical_Supplies = LebuMedicine.objects.filter(Category='Medical_Supplies').count()
        left_time = 0

        import datetime
        for v in medicine:
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
                exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                exdates = exdates.days
            v.exdate = exdates
            v.Days = days
            v.Expired_Date = left_time

        context = {'left_time':left_time, 'medicine':medicine, 'total_num':total_num, 'minerals':Minerals, 
                'cosmotics':Cosmotics, 'GIT':GITs, 'CNS':CNSs,'ENT':ENTs,
                'CVS':CVSs, 'hormones':Hormones, 'Anti_virals':Anti_virals, 
                'Anti_infectives':Anti_infectives, 'Anti_helmentics':Anti_helmentics,
                'maskuloskeletal':Maskuloskeletal, 'Medical_Supplies':Medical_Supplies }
        return render(request,'lebu_branch.html', context)
    else:
        return redirect('login')
    
def jemo_branch(request):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist'):
        medicine = JemoMedicine.objects.all().order_by('Name')

        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notificate = notify_msg.count()       
        medicine = JemoMedicine.objects.all().order_by('Name')
        total_num = medicine.count()

        Cosmotics = JemoMedicine.objects.filter(Category='Cosmotics', Branch="Jemo").count()
        GITs = JemoMedicine.objects.filter(Category='GIT', Branch="Jemo").count()
        CNSs = JemoMedicine.objects.filter(Category='CNS', Branch="Jemo").count()
        ENTs= JemoMedicine.objects.filter(Category='ENT', Branch="Jemo").count()
        CVSs = JemoMedicine.objects.filter(Category='CVS', Branch="Jemo").count()
        Minerals = JemoMedicine.objects.filter(Category='Minerals', Branch="Jemo").count()
        Hormones = JemoMedicine.objects.filter(Category='Hormones', Branch="Jemo").count()
        Anti_virals = JemoMedicine.objects.filter(Category='Anti_virals', Branch="Jemo").count()
        Anti_infectives = JemoMedicine.objects.filter(Category='Anti_infectives', Branch="Jemo").count()
        Anti_helmentics = JemoMedicine.objects.filter(Category='Anti_helmentics', Branch="Jemo").count()
        Maskuloskeletal = JemoMedicine.objects.filter(Category='Maskuloskeletal', Branch="Jemo").count()
        Medical_Supplies = JemoMedicine.objects.filter(Category='Medical_Supplies', Branch="Jemo").count()
        
        left_time = 0
        import datetime
        
        for v in medicine:   
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
                exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                exdates = exdates.days
            v.exdate = exdates
            v.Days = days
            v.Expired_Date = left_time

        context = {'left_time':left_time, 'medicine':medicine, 'total_num':total_num, 'minerals':Minerals, 
                'cosmotics':Cosmotics, 'GIT':GITs, 'CNS':CNSs,'ENT':ENTs,
                'CVS':CVSs, 'hormones':Hormones, 'Anti_virals':Anti_virals, 
                'Anti_infectives':Anti_infectives, 'Anti_helmentics':Anti_helmentics,
                'maskuloskeletal':Maskuloskeletal, 'Medical_Supplies':Medical_Supplies, 'notice':notificate }
        return render(request,'jemo_branch.html', context)
    else:
        return redirect('login')
    
def main_branch(request):
    if (request.user.is_authenticated and request.user.profile.position == 'Druggist'):
       
        notify_msg = Message.objects.filter(recv_name=request.user.username)
        notify_msg = notify_msg.filter(status='unread').all()
        notificate = notify_msg.count()       
        medicine = Medicine.objects.filter(Branch="Head Office").all()
        total_num = medicine.count()

        Cosmotics = Medicine.objects.filter(Category='Cosmotics', Branch="Head Office").count()
        GITs = Medicine.objects.filter(Category='GIT', Branch="Head Office").count()
        CNSs = Medicine.objects.filter(Category='CNS', Branch="Head Office").count()
        ENTs= Medicine.objects.filter(Category='ENT', Branch="Head Office").count()
        CVSs = Medicine.objects.filter(Category='CVS', Branch="Head Office").count()
        Minerals = Medicine.objects.filter(Category='Minerals', Branch="Head Office").count()
        Hormones = Medicine.objects.filter(Category='Hormones', Branch="Head Office").count()
        Anti_virals = Medicine.objects.filter(Category='Anti_virals', Branch="Head Office").count()
        Anti_infectives = Medicine.objects.filter(Category='Anti_infectives', Branch="Head Office").count()
        Anti_helmentics = Medicine.objects.filter(Category='Anti_helmentics', Branch="Head Office").count()
        Maskuloskeletal = Medicine.objects.filter(Category='Maskuloskeletal', Branch="Head Office").count()
        Medical_Supplies = Medicine.objects.filter(Category='Medical_Supplies', Branch="Head Office").count()
        left_time = 0
        day = 0

        import datetime
        for v in medicine:
            if v.Expired_Date:
                exdate = v.Expired_Date
                now = datetime.datetime.now()
                left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                left_time = left_time.days / 30
                left_time = int(left_time)
                now = datetime.datetime.now()

                days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                days = days.days % 30
                days = days
                exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
                exdates = exdates.days
            v.exdate = exdates
            v.Days = days
            v.Expired_Date = left_time

        context = {'day':day, 'left_time':left_time, 'medicine':medicine, 'total_num':total_num, 'minerals':Minerals, 
                'cosmotics':Cosmotics, 'GIT':GITs, 'CNS':CNSs,'ENT':ENTs,
                'CVS':CVSs, 'hormones':Hormones, 'Anti_virals':Anti_virals, 
                'Anti_infectives':Anti_infectives, 'Anti_helmentics':Anti_helmentics,
                'maskuloskeletal':Maskuloskeletal, 'Medical_Supplies':Medical_Supplies, 'notice':notificate }
        return render(request,'main_branch.html', context)
    else:
        return redirect('login')
    
# def add_druginJemo(request):
#     left_time = 0
#     import datetime
#     jemo_branch = Medicine.objects.filter(Branch='Head Office').all().order_by("Name")
#     for v in jemo_branch:
#         if v.Expired_Date:
#             exdate = v.Expired_Date
#             now = datetime.datetime.now()
#             left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
#             left_time = left_time.days / 30
#             left_time = int(left_time)
#             now = datetime.datetime.now()

#             days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
#             days = days.days % 30
#             days = days
#             exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
#             exdates = exdates.days
#         v.exdate = exdates
#         context = {"jemo_branch": jemo_branch}
#         return render(request, "add_druginJemo.html", context)

def add_druginJemo(request):
    left_time = 0
    import datetime
    druginjemo = Medicine.objects.filter(Branch='Head Office').all().order_by("Name")

    for v in druginjemo:
        if v.Expired_Date:
            exdate = v.Expired_Date
            now = datetime.datetime.now()
            left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
            left_time = left_time.days / 30
            left_time = int(left_time)
            now = datetime.datetime.now()

            days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
            days = days.days % 30
            days = days
            exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
            exdates = exdates.days
        v.exdate = exdates
    context = {"jemo_branch": druginjemo}
    return render(request, "add_druginJemo.html", context)

def add_druginLebu(request):
    left_time = 0
    import datetime
    druginlebu = Medicine.objects.filter(Branch='Head Office').all().order_by("Name")

    for v in druginlebu:
        if v.Expired_Date:
            exdate = v.Expired_Date
            now = datetime.datetime.now()
            left_time = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
            left_time = left_time.days / 30
            left_time = int(left_time)
            now = datetime.datetime.now()

            days = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
            days = days.days % 30
            days = days
            exdates = exdate.replace(tzinfo=None)  - now.replace(tzinfo=None) 
            exdates = exdates.days
        v.exdate = exdates
    context = {"lebu_branch": druginlebu}
    return render(request, "add_druginLebu.html", context)

def add_druginMainBranch(request):
    return render(request, "add_druginMainBranch.html")
    
######end drug Branches #####

def ENT(request):
    ENTs = Medicine.objects.filter(Category='ENT').all()
    context = {'ENT':ENTs}
    return render(request,'../templates/category/ENT.html',context)

def CNS(request):
    CNSs = Medicine.objects.filter(Category='CNS').all()
    return render(request,'../templates/category/CNS.html',{'CNSs':CNSs})

def GIT(request):
    GITs = Medicine.objects.filter(Category='GIT').all()
    context = {'GIT':GITs}
    return render(request,'../templates/category/GIT.html', context)

def CVS(request):
    CVSs = Medicine.objects.filter(Category='CVS')
    return render(request,'../templates/category/CVS.html',{'CVSs':CVSs})

def Vitamins(request):
    Vitamins = Medicine.objects.filter(Category='Vitamins')
    return render(request,'../templates/category/Vitamins.html',{'Vitamins':Vitamins})

def Cosmotics(request):
    Cosmotics = Medicine.objects.filter(Category='Cosmotics')
    return render(request,'../templates/category/Cosmotic.html',{'Cosmotics':Cosmotics})

def Minerals(request):
    Minerals = Medicine.objects.filter(Category='Minerals')
    return render(request,'../templates/category/Minerals.html',{'Minerals':Minerals})

def Hormones(request):
    Hormones = Medicine.objects.filter(Category='Hormones')
    return render(request,'../templates/category/Hormones.html',{'Hormones':Hormones})

def Anti_virus(request):
    Anti_virals = Medicine.objects.filter(Category='Anti_virals')
    context = {'Anti_virals':Anti_virals}
    return render(request,'../templates/category/Anti_virals.html',context)

def Anti_infectives(request):
    Anti_infectives = Medicine.objects.filter(Category='Anti_infectives')
    return render(request,'../templates/category/Anti_infectives.html',{'Anti_infectives':Anti_infectives})

def Anti_helmentics(request):
    Anti_helmentics = Medicine.objects.filter(Category='Anti_helmentics')
    return render(request,'../templates/category/Anti_helmentics.html',{'Anti_helmentics':Anti_helmentics})

def Maskuloskeletal(request):
    Maskuloskeletal = Medicine.objects.filter(Category='Maskuloskeletal')
    return render(request,'../templates/category/Maskuloskeletal.html',{'Maskuloskeletal':Maskuloskeletal})

def Medical_Supplies(request):
    Medical_Supplies = Medicine.objects.filter(Category='Medical_Supplies')
    return render(request,'../templates/category/Medical_Supplies.html',{'Medical_Supplies':Medical_Supplies})



def search_user(request, id):
    if request.user.is_authenticated and request.user.profile.position == 'System Admin':
        users = User.objects.all().order_by('username')
        user_no = User.objects.all().count()
        no_of_customers = Profile.objects.filter(position="Customer").all().count()
        no_of_users = user_no - no_of_customers
        feedback = Feedback.objects.all().order_by('date')
     
        search_user = User.objects.get(pk=id)
        context = {'users':users, 'feedback':feedback, 'no_of_customers':no_of_customers, 'no_of_users':no_of_users,'search':search_user}
        return render(request,'userUpdate.html', context)
    else:
        return redirect('login')
    
        
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.profile.position == 'System Admin':

        users = User.objects.all().order_by('username')
        user_no = User.objects.all().count()
        no_of_customers = Profile.objects.filter(position="Customer").all().count()
        no_of_users = user_no - no_of_customers

        feedback = Feedback.objects.all().order_by('date')
        success = True
        context = {'users':users, 'feedback':feedback, 'no_of_customers':no_of_customers, 'no_of_users':no_of_users, 'success':success}
        if 'userDelete' in request.POST:
                userid = request.POST.get('select_user')
                User.objects.filter(pk=userid).delete()
                Profile.objects.filter(user_id=userid).delete()
                return render(request,'dashboard.html', context)
    
        if 'addUser' in request.POST:
            fname = request.POST.get('fname')
            fname = fname.upper()
            lname = request.POST.get('lname')
            lname = lname.upper()
            username = request.POST.get('username')
            email = request.POST.get('email')
            branch = request.POST.get('branch')
            tele = request.POST.get('tele')
            gender = request.POST.get('gender')
            salary = request.POST.get('salary')
            position = request.POST.get('position')
            password = request.POST.get('password')
            conf_password = request.POST.get('confirm_password')
            success = True
            added = True
 
            context = {'fname': fname,"lname":lname,"username":username,"password":password, "email":email,
                            "branch":branch,"tele":tele, "gender":gender, "salary":salary, "position":position, 
                            "users":users,"user_no":user_no,"no_of_customers":no_of_customers, "no_of_users":no_of_users,"feedback":feedback,
                            'added':added}
            if User.objects.filter(username=username).exists():
                messages.success(request, "Username already exists")
                return render(request, 'addUser.html', context)
            elif password.__len__() < 8:
                messages.success(request, "Password should be more than 8 characters")
                return render(request, 'addUser.html', context)
            elif password != conf_password:
                messages.success(request, "Password does not match")
                return render(request, 'addUser.html', context)
            elif tele.__len__() != 12:
                messages.success(request, "enter the correct phone number")
                return render(request, 'addUser.html', context)    
            elif Profile.objects.filter(tele=tele).exists():
                messages.success(request, "phone number already exists")
                return render(request, 'addUser.html', context)   
            elif User.objects.filter(email=email).exists():
                messages.success(request, "email already exists")
                return render(request, 'addUser.html', context)            
            else:
                password = make_password(password)
                User.objects.create(username=username, last_name=lname, first_name=fname, email=email, password=password,
                                                    is_superuser='False', is_staff='False', is_active='True').save()
                Profile.objects.create(user=User.objects.get(username=username), tele=tele,
                                    branch=branch, gender=gender, salary=salary, position=position).save()
                messages.success(request, "Successfully added")
                return render(request,'addUser.html', context)
            
        if 'userUpdate' in request.POST:
            userid = request.POST.get('userid')
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            email = request.POST.get('email')
            branch = request.POST.get('branch')
            tele = request.POST.get('tele')
            gender = request.POST.get('gender')
            salary = request.POST.get('salary')
            position = request.POST.get('position')
            updated = True

            
            context = {'fname': fname,"lname":lname, "email":email,
                            "branch":branch,"tele":tele, "gender":gender, "salary":salary, "position":position, 
                            "users":users,"user_no":user_no,"no_of_customers":no_of_customers, "no_of_users":no_of_users,"feedback":feedback,
                             'updated':updated}

            phone = len(tele)
            if fname is not None and lname is not None and email is not None and branch is not None and salary is not None and position is not None:
                if phone != 12:
                    messages.success(request, "phone number length must be 12")
                    return render(request, 'userUpdate.html', context) 
                # elif Profile.objects.filter(tele=tele).exists():
                #     messages.success(request, "phone number already exists")
                #     return render(request, 'userUpdate.html', context) 
                # elif User.objects.filter(email=email).exists():
                #     messages.success(request, "email already exists")
                #     return render(request, 'userUpdate.html', context)  
                else:#+251978481098
                    User.objects.filter(pk=userid).update(last_name=lname, first_name=fname, email=email)
                    Profile.objects.filter(user_id=userid).update(tele=tele, branch=branch, gender=gender, salary=salary, position=position)
                   
                    messages.success(request, "Successfully updated")
                    return render(request, 'userUpdate.html', context)
            else: 
                messages.error(request, "Please fill all fields with")
                return render(request,'userUpdate.html', context)
 
        return render(request,'dashboard.html', context)

    else:
        return redirect('login')


def feedback(request):
    if request.user.is_authenticated and request.user.profile.position == 'Customer':
        feedback = request.POST.get('feedback')
        sender = request.POST.get('sender')

        if feedback != "":
            Feedback.objects.create(message=feedback, sender=sender).save()
            messages.info(request, "Thank you for your feedback!!!")
            return render(request, 'contactUs.html')
        else:
            return render(request, 'contactUs.html')
    else:
        return redirect('login')
    
    
def clear_msg(request):
    if request.user.is_authenticated:
        message = request.POST.get('message')
        clear_msg = Message.objects.filter(msg=message)
        for clear in clear_msg:
            if clear.recv_name==request.user.username or clear.send_name==request.user.username:
                clear_msg.delete()
        return redirect('clear_msg')

    else:
        return redirect('login')
    





#####SENDING SMS MESSAGES #####
# import datetime
# from twilio.rest import Client

# drug1 = Medicine.objects.all()
# drug2 = LebuMedicine.objects.all()
# drug3 = JemoMedicine.objects.all()

# for drug1 in drug1:
#     date1 = datetime.datetime.now()
#     date1 = int(date1.strftime('%Y%m%d'))
#     exdate1 = drug1.Expired_Date
#     # exdate = parse_date(exdate)
#     exdate1 = int(exdate1.strftime('%Y%m%d'))
    
# for drug2 in drug2:
#     date2 = datetime.datetime.now()
#     date2 = int(date2.strftime('%Y%m%d'))
#     exdate2 = drug2.Expired_Date
#     # exdate = parse_date(exdate)
#     exdate2 = int(exdate2.strftime('%Y%m%d'))

# for drug3 in drug3:
#     date3 = datetime.datetime.now()
#     date3 = int(date3.strftime('%Y%m%d'))
#     exdate3 = drug3.Expired_Date
#     # exdate = parse_date(exdate)
#     exdate3 = int(exdate3.strftime('%Y%m%d'))
# if date1 < exdate1 or date2 < exdate2 or date3 < exdate3:
#     user = Profile.objects.filter(position="Druggist")
#     for user in user:
#         code = "+" + user.tele
#         account_sid = 'ACd07b49824d53ad1d9f0618657107e4b9'
#         auth_token = 'db707cd2399c42336917c876668958fc'

#         client = Client(account_sid, auth_token)

#         message = client.messages.create(
#         from_='+12033072788',#12033072788
#         body = 'Hay! there is expired drug. Please check it now!',
#         to=code)

#     print(message.sid)
             
############rest_framework##########
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from django.http import JsonResponse
from .serializer import * 

class MedicineList(APIView):
    def get(self,request):
        import datetime
        medicine = Medicine.objects.all()     
        serializer = MedicineSerializer(medicine, many=True)
        return Response(serializer.data)
    

class JemoMedicineList(APIView):
    def get(self, request):
        J_medicine = JemoMedicine.objects.all()
        serializer = JemoMedicineSerializer(J_medicine, many=True)
        return Response(serializer.data)
    
class LebuMedicineList(APIView):
    def get(self, request):
        L_medicine = LebuMedicine.objects.all()
        serializer = LebuMedicineSerializer(L_medicine, many=True)
        return Response(serializer.data)


# class UserList(APIView):
#     def get(self,request):
#         user =  User.objects.all()
#         serializer =  UserSerializer(user, many=True)
#         return Response(serializer.data)
#     def post(self,request):
 
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else: 
#             return Response(serializer.errors)
#     def put(self, request, pk):
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#          user = User.objects.get(pk=pk)
#          user.delete()
#          return Response({"delete":"deleted successfully!!!"}) 

# class AddUser(APIView):
#         def post(self,request):
#             self.http_method_names.append("GET")

#             serializer = UserSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             else: 
#                 return Response(serializer.errors)

# class UpdateUser(APIView):            
#     def put(self, request, pk):
#         self.http_method_names.append("GET")

        # user = User.objects.get(pk=pk)
        # serializer = UserSerializer(user, many=False)
        
        # return Response(serializer.data)
     
            
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.permissions import AllowAny

class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    
# from django.http import HttpResponse
# from django.template.loader import get_template
# # from xhtml2pdf import pisa
# from io import BytesIO

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def some_view(request):
#     context = {'myvar': 'Hello World'}
#     pdf = render_to_pdf('pro.html', context)
#     return HttpResponse(pdf, content_type='application/pdf')

# class CreateMedicine(APIView):
#     def get(self, request):
#         drug = [ {"Name": med.Name,"Image": med.Image.url,
#              "Batchno":med.Batch_Number, "Exp_date":med.Expired_Date,
#              "price":med.Unit_Price, "Desc":med.Description} 
#         for med in Medicine.objects.filter(pk=14)
#         ]
#         return Response(drug)
  
#     def post(self,request):
#         serializer = MedicineSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else: 
#             return Response(serializer.errors)

# class Medicines(APIView):   
#     def get(self,request, pk):
#         try:
#              medicine = Medicine.objects.get(pk=pk)
#         except: 
#             return Response({
#                 "error":"book does not exist"
#             },status=status.HTTP_404_NOT_FOUND)   
    
#         serializer = MedicineSerializer(medicine, many=False)
#         if serializer:
#               return Response(serializer.data)
#         else:
#               return Response(serializer.errors)
          
#     def put(self, request, pk):
#         medicine = Medicine.objects.get(pk=pk)
#         serializer = MedicineSerializer(medicine, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#          medicine = Medicine.objects.get(pk=pk)
#          medicine.delete()
#          return Response({"delete":"deleted successfully!!!"})  

# class CustomerList(APIView):
#     def get(self,request):
#         medicine = Customer.objects.all()
#         serializer = customerSerializer(medicine, many=True)
#         return Response(serializer.data)
    
# class CreateCustomer(APIView):
  
#     def post(self,request):
#         serializer = customerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else: 
#             return Response(serializer.errors)
    
# class CustomerChange(APIView):  
#     def get(self,request, pk):
#         try:
#              customer = Customer.objects.get(pk=pk)
#         except: 
#             return Response({
#                 "error":"customer does not exist"
#             },status=status.HTTP_404_NOT_FOUND)   
    
#         serializer = customerSerializer(customer, many=False)
#         if serializer:
#               return Response(serializer.data)
#         else:
#               return Response(serializer.errors)
          
#     def put(self, request, pk):
#         customer = Customer.objects.get(pk=pk)
#         serializer = customerSerializer(customer, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#          customer = Customer.objects.get(pk=pk)
#          customer.delete()
#          return Response({"delete":"deleted successfully!!!"})  
    

    
# class UserChange(APIView):  
#     def get(self,request, pk):
#         try:
#              user = User.objects.get(pk=pk)
#         except: 
#             return Response({
#                 "error":"User does not exist"
#             },status=status.HTTP_404_NOT_FOUND)   
    
#         serializer = userSerializer(user, many=False)
#         if serializer:
#               return Response(serializer.data)
#         else:
#               return Response(serializer.errors)
          
#     def put(self, request, pk):
#         user = User.objects.get(pk=pk)
#         serializer = userSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#          user = User.objects.get(pk=pk)
#          user.delete()
#          return Response({"delete":"deleted successfully!!!"})  