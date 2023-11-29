import os
import subprocess
    
def resetInfo (): 
    
    if os.path.exists("../out"):
        try:
            subprocess.run(["rm", "-fr", "../out"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in removing the existing directory: {e}")

    print ("reset dataset and ./out folder")
    quit()
    
def checkWineTz (arg, data): 
    
    match arg: 

        case 1: 
            if float(data[0]) > float(data[1]): 
                print (f"ERROR 01 - Loading Price {data[0]} > {data[1]} .\n")
                quit()
        
        case 2: 
            if data[1].empty: 
                print (f"ERROR 02 - {data[0]} Dataframe")
                quit()

        case _: 
            print ("\nUNKNOW ERROR XY")
            quit ()
