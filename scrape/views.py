from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as bs
import json
import lxml

# Create your views here.




class Job:

    instances = []

    
        

    def __init__(self,title,company,location,link=None):
        self.title = title
        self.company = company
        self.location = location
        self.instances.append(self)
        self.link = link

def get_job_title_and_location(request):

    Job.instances = []

    if request.method == 'POST':
        job_title_space =  request.POST.get('job_name')
        job_title = job_title_space.replace(' ', '+')

        location_space = request.POST.get('location_name')
        location = location_space.replace(' ', '+')

        
        
        
        get_html_response_indeed(job_title,location)
        get_html_response_linkedin(job_title_space, location_space)
        get_html_response_monster(job_title_space, location_space)

        context = {'jobs': Job.instances}

        return HttpResponse(get_results(request,context))


        

        

        

    
       
    return render(request, 'scrape/scrape.html', {'jobs': Job.instances})

def get_html_response_indeed(job_title, location):

    indeed_link = f'https://www.indeed.com/jobs?q={job_title}&l={location}'

    s = requests.Session()

    html_data = s.get(indeed_link)

    html_data = html_data.content

    file1 = open('test.html', 'w')
    file1.write(str(html_data))
    file1.close()

    soup = bs(html_data, 'lxml')
    
    soup.prettify()
    
    if soup != None:
    
        mydivs = soup.select("body > table#resultsBody > tbody >tr > td > table ")[0].select('div.result')




    for i in mydivs:
        title = (i.find('a', {'class': 'jobtitle turnstileLink'}))

        company = (i.find('span', {'class': 'company'})).text
        
        print('LOCATION', location)


        location = (i.find('span', {'class': 'location'})).text
        


       

        Job(title.text, company, location, f"https://indeed.com{title['href']}")
           

    


    return 


def get_html_response_linkedin(job_title, location):
   
    linkedin_link = f'https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}'

    s = requests.Session()

    html_data = s.get(linkedin_link)

    html_data = html_data.content

    soup = bs(html_data, 'html.parser')

 
    


    titles = soup.find_all('a',{'class':'result-card__full-card-link'})

    companies = soup.find_all('a', {'class': 'result-card__subtitle-link job-result-card__subtitle-link' } )

    locations = soup.find_all('span', {'class':'job-result-card__location'})




    

 



    



    for i,j,k in zip(titles, companies, locations):
        Job(i.text,j.text,k.text, i["href"])



    


    # for i in linkedin_jobsarray:
    #     values = vars(i)
    #     print('\n\n\n\n')
    #     print('LINKEDIN')

    #     print (values['title'])
    #     print (values['company'])
    #     print (values['location'])
    #     print (values['summary'])
    #     print (values['link'])

    
    
    
def get_html_response_monster(job_title, location):
    monster_link =  f'https://services.monster.io/jobs-svx-service/v2/monster/jobs-search/samsearch/en-us'

    

    data = {"jobQuery":{"locations":[{"address":location,"country": 'us'}],"excludeJobs":[],"companyDisplayNames":[],"query":job_title,"employmentTypes":[]},"offset":0,"pageSize":10,"searchId":"","fingerprintId":"7effdce6f8d233f79d467aeac972bfc5","jobAdsRequest":{"position":[1,2,3,4,5,6,7,8,9,10],"placement":{"component":"JSR_SPLIT_VIEW","appName":"monster"}}}



    s = requests.Session()

    response = s.post(monster_link, json = data).json()

    

    jobresults_array = (response.get('jobResults'))

  


    for i in range(0, len(jobresults_array)):



        monster_job_title = (jobresults_array[i].get('jobPosting').get('title'))

        monster_job_company = (jobresults_array[i].get('jobPosting').get('hiringOrganization').get('name'))
        
        monster_job_city = (jobresults_array[i].get('jobPosting').get('jobLocation')[0].get('address').get('addressLocality'))
        monster_job_country =  (jobresults_array[i].get('jobPosting').get('jobLocation')[0].get('address').get('addressCountry'))
     

        monster_job_link = (jobresults_array[i].get('jobPosting').get('url'))

        monster_job_location =  (monster_job_city + ' ' + monster_job_country)

        

        


        

       
        
        

        Job(monster_job_title,monster_job_company,monster_job_location,monster_job_link)

    
    

        

def get_results(request, context):
    
    if request.method == 'POST' and 'LOL' in request.POST:
        return render(request, 'scrape/results.html', context)

    if request.method == 'POST' and 'results-page' in request.POST:

        Job.instances = []

        job_title_space =  request.POST.get('job_name')
        job_title = job_title_space.replace(' ', '+')

        location_space = request.POST.get('location_name')
        location = location_space.replace(' ', '+')

        
        
        
        get_html_response_indeed(job_title,location)
        get_html_response_linkedin(job_title_space, location_space)
        get_html_response_monster(job_title_space, location_space)

        return render(request, 'scrape/results.html', {'jobs' :Job.instances})

def get_starred(request):

    return render(request, 'scrape/starred.html')










    

    

    
    


   

    
    
