import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Creating a class called My_Chrome that overrides the __del__(self) method in uc.chrome class
#   This allows the browser to not automatically terminate
class My_Chrome(uc.Chrome):
    def __del__(self):
        pass

# setting up Options and adding path to existing profile -> We do this so we keep the history, cookies and cache for NG login
options = uc.ChromeOptions()

# CODE TO RUN SELENIUM IN HEADLESS MODEE
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# options.headless = True
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--no-proxy-server")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# END OF SELENIUM CODE IN HEADLESS MODE

options.add_argument('--user-data-dir=C:\\Users\\zimac\\AppData\\Local\\Google\\Chrome\\User Data')
# options.add_argument('--no-first-run --no-service-autorun --password-store=basic')  #This code is iffy, I don't know what it does

# Setting up driver as chrome object with profile setting using "options"
driver = My_Chrome(executable_path="C:\\Program Files\\Python39\\Scripts\\chromedriver.exe",options=options)
print("Welcome: Executing the Virgin Pulse Script...")  

#   METHOD TO TRACK TOP 3 HEALTHY HABITS, INPUT SLEEP HOURS AND INPUT STEPS
def trackHabitSleepSteps(driver):
    # driver.get("https://app.member.virginpulse.com/?kc_idp_hint=national-grid#/healthyhabits")
    driver.get("https://app.member.virginpulse.com/?kc_idp_hint=national-grid#/healthyhabits")
    # driver.find_element(By.XPATH,"//a[@href='https://member.virginpulse.com/login.aspx']").click()
    driver.implicitly_wait(10)  # We wait 10 seconds here for page to load to grab elements
    
    # Clicking "Yes" on the top 3 of the healthy habits 
    driver.find_element(By.ID,"tracker-639-track-yes").click()  
    driver.find_element(By.ID,"tracker-6059-track-yes").click() 
    driver.find_element(By.ID,"tracker-6060-track-yes").click() 
    print("1. The top 3 healthy habits have been tracked!!")

    # Inputting 8 hours as sleep and submitting
    driver.find_element(By.ID, "sleepHours").send_keys(8)   
    driver.find_element(By.ID, "track-sleep").click()       
    print("2. Your sleep of 8 hours have been tracked!")

    # Finds the "Steps" input box and enters 20000 and clicks submit.
    driver.find_element(By.ID, "numberOfSteps").send_keys(20000)    #
    driver.find_element(By.ID, "track-steps").click()
    print("3. Your steps have been tracked! ")


#   METHOD TO CLICK ON ALL AVAILABLE DAILY CARDS
def dailyCards(driver):
    driver.execute_script("window.open('https://app.member.virginpulse.com/?kc_idp_hint=national-grid#/home')") #Opens new tab
    driver.switch_to.window(driver.window_handles[1])   # Switches control to the new tab window
    print("Waiting 12 seconds..")
    time.sleep(8)  # Sleep for 12 seconds to allow trophy medal to pop up
    # Code to exit trophy pop up
    trophyMedal = driver.find_elements(By.ID, "trophy-modal-close-btn")
    if trophyMedal:
        trophyMedal[0].click()                                                     
    totalCards = len(driver.find_elements(By.XPATH,"//*[contains(@class,'stack-card ng-scope stack-card')]")) #Grab length of stack
    for _ in range(totalCards - 1):
        driver.implicitly_wait(.1)  #Significantly speeds up code
        trueButton = driver.find_elements(By.XPATH,"//button[@class='quiz-true-false-buttons vp-button bordered vp-button-primary-inverse ng-scope']")                                                              
        dailyClick = driver.find_elements(By.ID, "triggerCloseCurtain")             
        if len(dailyClick) > 0:                              
            dailyClick[0].click()
        if len(trueButton) > 0:
            trueButton[0].click()
            driver.implicitly_wait(5)
            driver.find_element(By.XPATH, "//button[@class='got-it-core-button ng-scope vp-button-primary']").click()                                                     # If there is a complete button, click it
        driver.find_element(By.XPATH, "//div[@class='next-card-btn ng-scope']").click() # Click next button 


# METHOD TO BROWSE RECIPE, TRACK CALORIE AND COMPLETE JOURNEY STEPS
def recipeCalorieJourney(driver):

    #   Browse recipes
    driver.execute_script("window.open('https://zipongo.com/home')")
    driver.switch_to.window(driver.window_handles[2])
    print("5. The recipe page have been browsed! ")

    #   Script to input calories
    driver.execute_script("window.open('https://www.myfitnesspal.com/food/quick_add?meal=1')")
    driver.switch_to.window(driver.window_handles[3])   
    driver.implicitly_wait(5)
    driver.find_element(By.ID,"ember1622").send_keys(2000)  # Grabs text box and inputs 2000 calories
    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()  # Grabs submit button and clicks it
    driver.find_element(By.CSS_SELECTOR,"a.button.complete-this-day-button").click()  # Grabs complete day button and clicks it
    print("6. Your calories of 2000 have been tracked!")

    #   Script to complete Journey Step
    driver.get("https://app.member.virginpulse.com/#/home")
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,"//a[@aria-label='Health']").click()   #Gets to the joruney page 
    # NewSteps grab all new journey steps but its amount is repeated on the bottom row hence we divide by 2
    newSteps = driver.find_elements(By.XPATH,"//*[contains(@aria-label,'One new step available')]")
    half = int(len(newSteps)/2)
    myJourneys = driver.find_elements(By.XPATH,"//a[@class='journey-tile-link']")
    # Iterates through available journey steps, opens them in a new tab and completes them and then closes it and returns.
    for x in myJourneys[:half]:
        x.send_keys(Keys.CONTROL + Keys.ENTER)
        driver.switch_to.window(driver.window_handles[4])
        driver.implicitly_wait(5)
        complete1 = driver.find_elements(By.XPATH,"//button[@class='got-it-core-button vp-button-primary ng-star-inserted']")
        complete2 = driver.find_elements(By.XPATH,"//button[@class='got-it-core-button vp-button-primary']")
        if len(complete1) > 0:
            complete1[0].click()
        if len(complete2) > 0:
            complete2[0].click()
        driver.implicitly_wait(.1)
        driver.close()
        driver.switch_to.window(driver.window_handles[3])
    print(f"7. Your {half} Journey Steps have been completed!")


# METHOD TO OPEN UP 'QUICK PICK ONE MINUTE WHIL SESSION'
def whilSession(driver):

    # Method to go grab top 7 videos and pick the 5th video which is 1 minute long
    driver.execute_script("window.open('https://connect.whil.com/')")
    driver.switch_to.window(driver.window_handles[4])
    time.sleep(10)
    quickPicks = driver.find_elements(By.XPATH, "//li[@class='css-4rbku5 css-1dbjc4n r-1loqt21 r-1otgn73 r-eafdt9 r-1i6wzkk r-lrvibr r-13qz1uu']")
    quickPicks[4].click()
    print("8. Your one minute whil session has opened! Wait 10 seconds for video to play..")


# Defining main method here with the 4 methods to be executed
def main():
    trackHabitSleepSteps(driver)
    dailyCards(driver)
    recipeCalorieJourney(driver)
    whilSession(driver)

# Executing Main function
if __name__ == "__main__":
    main()
