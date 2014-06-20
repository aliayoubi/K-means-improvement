# -*- encoding:utf-8
from __future__ import unicode_literals

from hazm import word_tokenize
from hazm import Stemmer
import math
import random
from hazm import Normalizer


def k_means(doc,number_of_clusters,numbers_of_iterations):
    
    literals=["به","با","از","در","بی","برای","چون","اندر","زیر","بر","الی","جز","الا","مگر","نزد","نزدیک","پیش","روی","میان","پی","جلوی","مانند","چون","درون","فراز","درباره ","محص","خاطر","نظر","راه","مثل","توسط","خلاف","دنبال","زعم","سبب","خلال","راه","سر","عین","وقت","هنگام","بجز","همچون","همچون","زیبا","قشنگ","روشن","مشخص","بزرگ","فوقالعاده","خوب","ناراحت","کوچک","مهربان","محبوب","معتقد","خوشگل","ممنون","سبک","موقت","احمق","شلوغ","مهم","جدید","بد","دور","کامل","موافق","مقارن","اجتماعی","معین","صادق","مسخره","غمگین","سرغ","خوشحال","مناسب","کند","زشت","پارسا","قدیمی","سخت","خوش","غریبه"]
    
    doc_list=doc_normalizer(doc)
    
    l_1=[]
    
    for i in range(len(doc_list)):
        l_1.append(word_tokenize(doc_list[i]))
    
    for i in range(len(l_1)):
        for word in l_1[i]:
            if word in literals:
                del word    
    l_2=doc_stemmer(l_1)
    
    l_vectors=[]
    for i in range(len(doc_list)):
        l_vectors.append([])
    
    for i in range(len(l_2)):#converting document to equivalent vector model
        for j in range(len(l_2[i])):
            l_vectors[i].append(w(l_2,l_2[i],l_2[i][j]))
    
    
    l_centeroids=[]
    for i in range(number_of_clusters):#generating random initial centeroids
        l_centeroids.append([])
    for i in range(len(l_centeroids)):
        for j in range(len(doc_list)):
            l_centeroids[i].append(random.random())    
        
    l_cosines=[]
    for i in range(len(l_vectors)):
        l_cosines.append([])
    for i in range(len(l_vectors)):
        for j in range(len(l_centeroids)):
            l_cosines[i].append(cosine(l_vectors[i], l_centeroids[j]))
            
    #print l_cosines  
    
    l_index=[]
    for i in range(len(l_cosines)):
        l_index.append([])
    
    for i in range(len(l_cosines)):
        for j in range(len(l_cosines[i])):
            if l_cosines[i][j]==min(l_cosines[i]):
                l_index[i].append(j)
                
    #print l_index                      
            
    l_clusters_1=[]
    l_clusters_2=[]
    l_clusters_vectors=[]
    for i in range(number_of_clusters):
        l_clusters_1.append([])
        l_clusters_2.append([])
        l_clusters_vectors.append([])        
    for i in range(len(l_index)):
        for j in range(len(l_index)):
            if l_index[i][0]==l_index[j][0] and j not in l_clusters_1[l_index[i][0]]:
                l_clusters_1[l_index[i][0]].append(j)
                l_clusters_2[l_index[i][0]].append(l_2[j])
                l_clusters_vectors[l_index[i][0]].append(l_vectors[j])
                
    #print l_clusters_1
    #print l_clusters_2
    #print l_clusters_vectors
    #print centeroid_generator(l_clusters_vectors) 
    
    iteration=0
    while iteration<numbers_of_iterations:
        l_centeroids_2=centeroid_generator(l_clusters_vectors)
        
        
        l_cosines_2=[]
        for i in range(len(l_vectors)):
            l_cosines_2.append([])
        for i in range(len(l_vectors)):
            for j in range(len(l_centeroids_2)):
                if l_centeroids_2[j]:
                    l_cosines_2[i].append(cosine(l_vectors[i], l_centeroids_2[j]))
        
        #print l_cosines_2           
        l_index_2=[]
        for i in range(len(l_cosines_2)):
            l_index_2.append([])
    
        for i in range(len(l_cosines_2)):
            for j in range(len(l_cosines_2[i])):
                if l_cosines_2[i][j]==min(l_cosines_2[i]):
                    l_index_2[i].append(j)
        
        
        l_clusters_1=[]
        l_clusters_2=[]
        l_clusters_vectors=[]
        for i in range(number_of_clusters):
            l_clusters_1.append([])
            l_clusters_2.append([])
            l_clusters_vectors.append([])        
        for i in range(len(l_index_2)):
            for j in range(len(l_index_2)):
                if l_index_2[i][0]==l_index_2[j][0] and j not in l_clusters_1[l_index_2[i][0]]:
                    l_clusters_1[l_index_2[i][0]].append(j)
                    l_clusters_2[l_index_2[i][0]].append(l_2[j])
                    l_clusters_vectors[l_index_2[i][0]].append(l_vectors[j]) 
                             
        iteration+=1            
        
    print l_clusters_vectors
    print l_clusters_1
    print l_clusters_2
    
def centeroid_generator(vectors_list):    
    new_centeroids=[]
    for i in range(len(vectors_list)):
        new_centeroids.append([])
    for i in range(len(vectors_list)):
        a=[]
        
        if vectors_list[i]:
            for j in range(len(vectors_list[i])):
            
                a.append(len(vectors_list[i][j]))
                
            for k in range(min(a)):
                m=0
                for z in range(len(vectors_list[i])):
                    m+=vectors_list[i][z][k]
                m=m/len(vectors_list[i])
                    
                new_centeroids[i].append(m)       
            
    return new_centeroids
        
                
                       
def doc_stemmer(doc):
    stem_doc_list=[]
    stemmer=Stemmer()
    for i in range(len(doc)):
        stem_doc_list.append([])
    for i in range(len(doc)):
        for j in range(len(doc[i])):
            stem_doc_list[i].append([])
            
                
    for i in range(len(doc)):
        for j in range(len(doc[i])):
            for z in range(len(doc[i][j])):
                stem_doc_list[i][j].append(stemmer.stem(doc[i][j][z]))           
    
    return stem_doc_list

def doc_normalizer(doc):
    normalized_doc_list=[]
    normalizer=Normalizer()
    for i in range(len(doc)):
        normalized_doc_list.append(normalizer.normalize(doc[i]))
                
    return normalized_doc_list
                    

    
    
def tf(text,term):
    
    count=0.0
    for s in text:
        if s==term:
            count+=1
    return count/len(text)

 

def idf(text_list,term):
    n=0
     
    for i in range(len(text_list)):
        if term in text_list[i]:
            n+=1   
    return math.log(len(text_list))/n

                    
                       
def cosine(v1,v2):
    sum1, sum2, suma = 0, 0, 0
    if len(v1)<=len(v2):
        for i in range(len(v1)):
            suma += v1[i]*v2[i]
            sum1 += v1[i]**2
            sum2 += v2[i]**2
            return suma/math.sqrt(sum1*sum2)
    else:
        for i in range(len(v2)):
            suma += v1[i]*v2[i]
            sum1 += v1[i]**2
            sum2 += v2[i]**2
        
        
        return suma/math.sqrt(sum1*sum2)       
            
def w(text_list_1,text_1,term_1):
    return tf(text_1, term_1)*idf(text_list_1, term_1)

a=['''مهندسی سخت‌افزار در مقطع کارشناسی به مطالعه و بررسی طراحی سخت‌افزاری، کنترل سخت‌افزاری و شبکه‌های کامپیوتری می‌پردازد. برای مثال یک مهندس سخت‌افزار می‌تواند طراحی سخت‌افزاری کند که با آی‌سیها کار کند، بوسیله نرم‌افزارهای طراحی خودکار همچون لئوناردو یا مکس پلاس و ... به طراحی آی سی‌های سفارشی بپردازد و آنها را بر روی fpga پیاده کند با کامپیوتر کار کند و یا از دروازه‌های کامپیوتر استفاده نماید و در نهایت می‌تواند به طراحی مدارهای مجتمع دیجیتالی بپردازد. که البته این بخش از سخت‌افزار بیشتر در مقطع کارشناسی ارشد و دکتری پرداخته می‌شود.
از جمله دروس این مهندسی در دوره لیسانس مدارهای منطقی، طراحی VLSI، معماری کامپیوتر، الکترونیک دیجیتال، میکروپروسسورها ، طراحی مدارهای واسط ، سیستم کنترل خطی ،زبان ماشین و برنامه نویسی سیستم ،ساختمان گسسته ،کاربرد کنترل کننده میکرو در اتوماسیون،مخابرات دیجیتال(انتقال داده ها)،کنترل صنعتی دیجیتال PLC،مسیریابی شبکه ، امنیت شبکه ،ریاضی مهندسی ، و غیره می‌باشد.'''
,'''مهندسی نرم‌افزار به مفهوم توسعه و بازبینی یک سامانه نرم‌افزاری مربوط می‌باشد. این رشته علمی با شناسایی، تعریف، فهمیدن و بازبینی خصوصیات مورد نیاز نرم‌افزار حاصل سر و کار دارد. این خصوصیات نرم‌افزاری ممکن است شامل پاسخگویی به نیازها، اطمینان‌پذیری، قابلیت نگهداری، در دسترس بودن، آزمون‌پذیری، استفاده آسان، قابلیت حمل و سایر خصوصیات باشد.
مهندسی نرم‌افزار ضمن اشاره به خصوصیات فوق، مشخصات معین طراحی و فنی را آماده می‌کند که اگر به‌درستی پیاده‌سازی شود، نرم‌افزاری را تولید خواهد کرد که می‌تواند بررسی شود که آیا این نیازمندی‌ها را تأمین می‌کند یا خیر.
مهندسی نرم‌افزار همچنین با خصوصیات پروسه توسعه نرم‌افزاری در ارتباط است. در این رابطه، با خصوصیاتی مانند هزینه توسعه نرم‌افزار، طول مدت توسعه نرم‌افزار و ریسک‌های توسعه نرم‌افزار درگیر است.'''
,'''دین، آیین، کیش یک جهان بینی و مجموعه‌ای از باورها است که می‌کوشد توضیحی برای یک رشته از پرسش‌های اساسی مانند چگونگی پدید آمدن اشیا و جانداران و آغاز و پایان احتمالی چیزها، و چگونه زیستن ارائه دهد. ادیان فراعقلی اند، یعنی بخش‌هایی از آن مستقل از عقل و بر مبنای عشق و اعتقاد است.
شمار دین‌ها در میان انسان‌ها بسیار زیاد است و این ادیان توضیحات بسیار متفاوت و داستان‌های پرشماری را در راه کوشش برای یافتن پاسخ به معماهای یاد شده مطرح می‌کنند.
در باور دینداران، موجود یا موجوداتی که فراتر از قوانین جاری طبیعت هستند این جهان را آفریده و بر آن فرمان‌روایی می‌کنند و انسان می‌تواند از راه پرستش او/آنان از واکنش آن موجود یا آن چند موجود استفاده نماید و به درجه‌ای از حس امنیت و آرامش برسد.[۱] درباره این‌که «موجود آفریننده» مورد نظر ادیان چه خصوصیاتی دارد و تعداد و صفات و اهداف آن‌ها چیست و طول عمر و ابعاد و شمار پیام‌آوران آن‌ها چه تعداد و اندازه‌است در میان ادیان اختلاف نظرهای بسیار زیادی وجود دارد.'''
,'''اسلام، دینی یکتاپرستانه[۱][۲]و از دین‌های ابراهیمی است.[۳][۴] به پیروان اسلام «مسلمان» می‌گویند.[۵] هم‌اکنون اسلام از دید شمار رسمی پیروان، در جایگاه دوم در جهان جای دارد.[۶]
مسلمانان براین باورند که خداوند، قرآن را به محمد از طریق فرشته ای به نام جبرئیل فروفرستاده‌است. به باور مسلمانان خدا بر بسیاری از پیامبران، وحی فرستاده و محمد آخرین آنان است. مسلمانان محمد را اعاده‌کننده ایمان توحیدی خالص ابراهیم، موسی، عیسی و دیگر پیامبران می‌دانند و معتقدند که اسلام کامل‌ترین و آخرین آیین الهی[۷][۸] است.
پال فریدمن می‌گوید: «اسلام به معنی تسلیم در برابر خداست. اسلام دین قانون و عمل است، نه ریاضت و رهبانیت. اسلام یک دین میانه‌رو است؛ تشویق به کمک به فقیران می‌کند ولی تشویق به ترک دنیا نمی‌کند. اسلام بر رفتار درست تاکید می‌کند: شراب‌خواری و قمار منع شده‌اند و مسلمان موظف است از خوردن غذای حرام خودداری کند. مسلمان می‌تواند مستقیماً با خدا راز و نیاز کند و لزوماً نیازی به واسطه فیض نیست. مسجد تنها مکان تجمع است و مانند کلیسا دارای قدرت مذهبی نیست. اسلام، برخلاف یهودیت، پس از ظهور به سرعت دینی جهانی می‌شود و مردم را به مسلمان‌شدن تشویق می‌کند ولی اصرار زیادی بر مسلمان‌کردن ندارد.»[۹]'''
,'''ادبیّات فارسی یا ادبیات پارسی به ادبیاتی گفته می‌شود که به زبان فارسی نوشته شده باشد. ادبیات فارسی تاریخی هزار و صد ساله دارد. شعر فارسی و نثر فارسی دو گونه اصلی در ادب فارسی هستند. برخی کتابهای قدیمی در موضوعات غیرادبی مانند تاریخ، مناجات و علوم گوناگون نیز دارای ارزش ادبی هستند و با گذشت زمان در زمره آثار کلاسیک ادبیات فارسی قرار گرفته‌اند.
ادبیات فارسی ریشه در ادبیات باستانی ایران دارد که تحت تاثیر متون اوستایی در دوران ساسانی به زبان‌های پارسی میانه و پهلوی اشکانی پدید آمد. ادبیات فارسی نو نیز پس از اسلام و با الگوبرداری از ادبیات عربی در نظم و ریشه‌های دبیری و نویسندگی دوران ساسانی که ادبیات منثور عربی را ایجاد کرده بود در زمینه نثر متولد شد. ادبیات شفاهی فارسی نیز به همان سبک باستانی خود ادامه یافت.
ادبیات فارسی موضوعاتی مانند حماسه و روایات و اساطیر ایرانی و غیر ایرانی، مذهب و عرفان، روایت‌های عاشقانه، فلسفه و اخلاق و نظایر آن را در برمی‌گیرد. حسب موضوع مورد کاربرد در یک آفریده ادبی فارسی آن را در حیطه ادبیات حماسی، غنایی، تعلیمی یا نمایشی قرار می‌گیرد.
ادبیات فارسی چهره‌های بین‌المللی شناخته شده‌ای دارد که بیشتر آن‌ها شاعران سده‌های میانه هستند. از این میان می‌توان به رودکی، فردوسی، نظامی، خیام، سعدی، مولانا و حافظ اشاره کرد.گوته معتقد است ادبیات فارسی، یکی از چهار ارکان ادبیات بشر است.[۱]''']

k_means(a,4,2) 
        