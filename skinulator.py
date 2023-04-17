import customtkinter
import random

# Avg prices for skins of different qualities and floats (battle-scarred, well-worn, field-tested, minimal wear, factory new)
avg_milspec = [0.54, 0.35, 0.27, 0.54, 1.21]
avg_stattrak_ms = [1.04, 1.22, 0.79, 1.28, 3.53]
avg_restricted = [2.35, 2.22, 2.08, 3.48, 6.99]
avg_stattrak_res = [5.61, 4.75, 4.68, 7.33, 15.95]
avg_classified = [9.93, 15.50, 11.11, 19.07, 40.72]
avg_stattrak_class = [25.63, 31.85, 30.88, 46.95, 93.35]
avg_covert = [16.31, 32.74, 74.29, 93.37, 146.38]
avg_stattrak_cov = [58.46, 81.41, 201.85, 251.85, 313.06]
avg_special = [746.05, 741.39, 772.05, 805.56, 821.10]
avg_stattrak_special = [770.40, 788.62, 820.71, 840.86, 956.77]

# Globals
prob = []
money_spent = 0.00
money_list = []
fallacy = 0.00
unlock_count = 0
wallet = 0.00

# Lists for probabilities, and results to be tracked.
win_rate_per_colour = [0.7992327, 0.1598465, 0.0319693, 0.0063939, 0.0025575]
stattrak = [0.07992327, 0.01598465, 0.00319693, 0.00063939, 0.00025575]
skinfloat = [0.55, 0.07, 0.23, 0.08, 0.07]
results = []
results.clear()

# Aggregated win rates for quality selection.
win_01 = win_rate_per_colour[0] + win_rate_per_colour[1]
win_012 = win_rate_per_colour[0] + win_rate_per_colour[1] + win_rate_per_colour[2]
win_0123 = win_rate_per_colour[0] + win_rate_per_colour[1] + win_rate_per_colour[2] + win_rate_per_colour[3]

# Aggregated win rates for stat-track.
st_01 = stattrak[0] + stattrak[1]
st_012 = stattrak[0] + stattrak[1] + stattrak[2]
st_0123 = stattrak[0] + stattrak[1] + stattrak[2] + stattrak[3]
st_01234 = stattrak[0] + stattrak[1] + stattrak[2] + stattrak[3] + stattrak[4]

# Aggregated skin float probabilities.
sf_01 = skinfloat[0] + skinfloat[1]
sf_012 = skinfloat[0] + skinfloat[1] + skinfloat[2]
sf_0123 = skinfloat[0] + skinfloat[1] + skinfloat[2] + skinfloat[3]
sf_01234 = skinfloat[0] + skinfloat[1] + skinfloat[2] + skinfloat[3] + skinfloat[4]

money_earned = []

# Colors class
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKRED = '\033[0;31m'
    ENDC = '\033[0m'

# Body of application.
class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        money_earned = 0.00

        self.geometry("500x500")
        self.title("Skinulator")
        self.minsize(500, 500)

        # Create grid system.
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure((0, 2), weight=2)

        # Setting up the UI of the application with the elements to draw.
        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")
        self.labelMoneySpent = customtkinter.CTkLabel(master=self, text_color='red', text="Money Spent: $" + str(money_spent))
        self.labelMoneySpent.grid(row=2, column=0, columnspan=1, padx=20, pady=20, sticky="nsew")
        self.labelMoneyEarned = customtkinter.CTkLabel(master=self, text_color='#05f709', text="Money Earned: $" + str(money_earned))
        self.labelMoneyEarned.grid(row=2, column=1, columnspan=1, padx=20, pady=20, sticky="nsew")
        self.labelFallacy = customtkinter.CTkLabel(master=self, text_color='#00d0ff', text="Fallacy: " + str(fallacy) + '%')
        self.labelFallacy.grid(row=2, column=2, columnspan=1, padx=20, pady=20, sticky="nsew")
        self.labelWallet = customtkinter.CTkLabel(master=self, text_color='#FFFFFF', text="Wallet: $ " + str(wallet))
        self.labelWallet.grid(row=3, column=0, columnspan=1, padx=20, pady=20, sticky="nsew")
        self.labelUnlockCount = customtkinter.CTkLabel(master=self, text_color='#FFFFFF', text="Unlock Count: #" + str(unlock_count))
        self.labelUnlockCount.grid(row=3, column=2, columnspan=1, padx=20, pady=20, sticky="nsew")
        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Unlock")
        self.button.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="Enter a number to auto unlock")
        self.entry.grid(row=5, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.buttonAuto = customtkinter.CTkButton(master=self, command=self.auto_unlock, text="Auto-Unlock")
        self.buttonAuto.grid(row=6, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.buttonReset = customtkinter.CTkButton(master=self, command=lambda: self.reset_skinulator('NONE'), text="Reset")
        self.buttonReset.grid(row=7, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

    # Tracking the gambler's fallacy.
    def gambler_fallacy(self, fallacy_value, last_reward):

        # Check if the last reward was a Special Item or not.
        if ('Special Item(Gold)' in last_reward):
            fallacy_value = 0.00
        else:
            accumulated_fallacy = 0.0025575 + 0.0063939 + 0.0319693 + \
                  (0.00319693 * 0.0319693) + (0.00063939 * 0.0063939) + (0.00025575 * 0.0025575)
            fallacy_value += accumulated_fallacy # Increment by the odds of the profitable item drops, since that is what people are looking for.
            fallacy_value = round(fallacy_value, 3)
            
            # Check if the fallacy value is greater than 100%, if so we lock it to 100%.
            if (fallacy_value >= 100):
                fallacy_value = 100
        return fallacy_value

    
    # Function to select the skinfloats.
    def skin_float(self):
        rand_skin_float = random.uniform(0, 1)
    
        if (0 <= rand_skin_float <= skinfloat[0]):
            return ' Battle-Scarred'
        elif (skinfloat[0] < rand_skin_float <= sf_01):
            return ' Well-Worn'
        elif (sf_01 < rand_skin_float <= sf_012):
            return ' Field-Tested'
        elif (sf_012 < rand_skin_float <= sf_0123):
            return ' Minimal Wear'
        else:
            return ' Factory New'

    # Function to select if the reward is stat-trak.
    def stat_trak(self, rewarded_qual):
        rand_stat_trak_select = random.uniform(0, 1)
    
        if (rewarded_qual == 'Mil-Spec(Blue)'):
            if (0 <= rand_stat_trak_select <= stattrak[0]):
                return 'Mil-Spec(Blue) Stat-Trak'
            else:
                return 'Mil-Spec(Blue)'
        elif (rewarded_qual == 'Restricted(Purple)'):
            if (0 <= rand_stat_trak_select <= stattrak[1]):
                return 'Restricted(Purple) Stat-Trak'
            else:
                return 'Restricted(Purple)'
        elif (rewarded_qual == 'Classified(Pink)'):
            if (0 <= rand_stat_trak_select <= stattrak[2]):
                return 'Classified(Pink) Stat-Trak'
            else:
                return 'Classified(Pink)'
        elif (rewarded_qual == 'Covert(Red)'):
            if (0 <= rand_stat_trak_select <= stattrak[3]):
                return 'Covert(Red) Stat-Trak'
            else:
                return 'Covert(Red)'
        elif (rewarded_qual == 'Special Item(Gold)'):
            if (0 <= rand_stat_trak_select <= stattrak[4]):
                return 'Special Item(Gold) Stat-Trak'
            else:
                return 'Special Item(Gold)'
    


    # This is the function that performs the simulated case unlocking reward.
    def case_unlock(self):
        rand_unlock_select = random.uniform(0, 1) # Generate random number between 0 and 1 for probabilities of unlocks.
        reward = '' # Setting reward to empty, this will change with the simulation.
        roll_st = '' # Setting to empty as it will be changed later on.
        sf = '' # Setting skin float to empty, will change in the sim later on.
        final = '' # Setting empty, changes later.
    
        # Check what item was won.
        if (0 <= rand_unlock_select <= win_rate_per_colour[0]):
            reward = 'Mil-Spec(Blue)'
            sf = self.skin_float()
            roll_st = self.stat_trak(reward)
            final = roll_st + sf
            return final
        elif (win_rate_per_colour[0] < rand_unlock_select <= win_01): # (win_rate_per_colour[0] + win_rate_per_colour[1])
            reward = 'Restricted(Purple)'
            sf = self.skin_float()
            roll_st = self.stat_trak(reward)
            final = roll_st + sf
            return final
        elif (win_01 < rand_unlock_select <= win_012):
            reward = 'Classified(Pink)'
            sf = self.skin_float()
            roll_st = self.stat_trak(reward)
            final = roll_st + sf
            return final
        elif (win_012 < rand_unlock_select <= win_0123):
            reward = 'Covert(Red)'
            sf = self.skin_float()
            roll_st = self.stat_trak(reward)
            final = roll_st + sf
            return final
        else:
            reward = 'Special Item(Gold)'
            sf = self.skin_float()
            roll_st = self.stat_trak(reward)
            final = roll_st + sf
            return final

    # Function to reward the player with money after an unlock.
    def money_mil_spec(self, item_won):
        money_won = 0.00
        if (item_won == 'Mil-Spec(Blue) Battle-Scarred'):
            money_won += avg_milspec[0]
        elif (item_won == 'Mil-Spec(Blue) Well-Worn'):
            money_won += avg_milspec[1]
        elif (item_won == 'Mil-Spec(Blue) Field-Tested'):
            money_won += avg_milspec[2]
        elif (item_won == 'Mil-Spec(Blue) Minimal Wear'):
            money_won += avg_milspec[3]
        elif (item_won == 'Mil-Spec(Blue) Factory New'):
            money_won += avg_milspec[4]
        elif (item_won == 'Mil-Spec(Blue) Stat-Trak Battle-Scarred'):
            money_won += avg_stattrak_ms[0]
        elif (item_won == 'Mil-Spec(Blue) Stat-Trak Well-Worn'):
            money_won += avg_stattrak_ms[1]
        elif (item_won == 'Mil-Spec(Blue) Stat-Trak Field-Tested'):
            money_won += avg_stattrak_ms[2]
        elif (item_won == 'Mil-Spec(Blue) Stat-Trak Minimal Wear'):
            money_won += avg_stattrak_ms[3]
        else:
            money_won += avg_stattrak_ms[4]
        print(money_won)
        return money_won

    # Function for rewarding the money for an item that is restricted.
    def money_restricted(self, item_won):
        money_won = 0.00
        if (item_won == 'Restricted(Purple) Battle-Scarred'):
            money_won += avg_restricted[0]
        elif (item_won == 'Restricted(Purple) Well-Worn'):
            money_won += avg_restricted[1]
        elif (item_won == 'Restricted(Purple) Field-Tested'):
            money_won += avg_restricted[2]
        elif (item_won == 'Restricted(Purple) Minimal Wear'):
            money_won += avg_restricted[3]
        elif (item_won == 'Restricted(Purple) Factory New'):
            money_won += avg_restricted[4]
        elif (item_won == 'Restricted(Purple) Stat-Trak Battle-Scarred'):
            money_won += avg_stattrak_res[0]
        elif (item_won == 'Restricted(Purple) Stat-Trak Well-Worn'):
            money_won += avg_stattrak_res[1]
        elif (item_won == 'Restricted(Purple) Stat-Trak Field-Tested'):
            money_won += avg_stattrak_res[2]
        elif (item_won == 'Restricted(Purple) Stat-Trak Minimal Wear'):
            money_won += avg_stattrak_res[3]
        else:
            money_won += avg_stattrak_res[4]
        print(money_won)
        return money_won

    # Function for rewarding the money for an item that is classified.
    def money_classified(self, item_won):
        money_won = 0.00
        if (item_won == 'Classified(Pink) Battle-Scarred'):
            money_won += avg_classified[0]
        elif (item_won == 'Classified(Pink) Well-Worn'):
            money_won += avg_classified[1]
        elif (item_won == 'Classified(Pink) Field-Tested'):
            money_won += avg_classified[2]
        elif (item_won == 'Classified(Pink) Minimal Wear'):
            money_won += avg_classified[3]
        elif (item_won == 'Classified(Pink) Factory New'):
            money_won += avg_classified[4]
        elif (item_won == 'Classified(Pink) Stat-Trak Battle-Scarred'):
            money_won += avg_stattrak_class[0]
        elif (item_won == 'Classified(Pink) Stat-Trak Well-Worn'):
            money_won += avg_stattrak_class[1]
        elif (item_won == 'Classified(Pink) Stat-Trak Field-Tested'):
            money_won += avg_stattrak_class[2]
        elif (item_won == 'Classified(Pink) Stat-Trak Minimal Wear'):
            money_won += avg_stattrak_class[3]
        else:
            money_won += avg_stattrak_class[4]
        print(money_won)
        return money_won
    
    # Function for rewarding the money for an item that is covert.
    def money_covert(self, item_won):
        money_won = 0.00
        if (item_won == 'Covert(Red) Battle-Scarred'):
            money_won += avg_covert[0]
        elif (item_won == 'Covert(Red) Well-Worn'):
            money_won += avg_covert[1]
        elif (item_won == 'Covert(Red) Field-Tested'):
            money_won += avg_covert[2]
        elif (item_won == 'Covert(Red) Minimal Wear'):
            money_won += avg_covert[3]
        elif (item_won == 'Covert(Red) Factory New'):
            money_won += avg_covert[4]
        elif (item_won == 'Covert(Red) Stat-Trak Battle-Scarred'):
            money_won += avg_stattrak_cov[0]
        elif (item_won == 'Covert(Red) Stat-Trak Well-Worn'):
            money_won += avg_stattrak_cov[1]
        elif (item_won == 'Covert(Red) Stat-Trak Field-Tested'):
            money_won += avg_stattrak_cov[2]
        elif (item_won == 'Covert(Red) Stat-Trak Minimal Wear'):
            money_won += avg_stattrak_cov[3]
        else:
            money_won += avg_stattrak_cov[4]
        print(money_won)
        return money_won
    
    # Function for rewarding the money for an item that is special.
    def money_special(self, item_won):
        money_won = 0.00
        if (item_won == 'Special Item(Gold) Battle-Scarred'):
            money_won += avg_special[0]
        elif (item_won == 'Special Item(Gold) Well-Worn'):
            money_won += avg_special[1]
        elif (item_won == 'Special Item(Gold) Field-Tested'):
            money_won += avg_special[2]
        elif (item_won == 'Special Item(Gold) Minimal Wear'):
            money_won += avg_special[3]
        elif (item_won == 'Special Item(Gold) Factory New'):
            money_won += avg_special[4]
        elif (item_won == 'Special Item(Gold) Stat-Trak Battle-Scarred'):
            money_won += avg_stattrak_special[0]
        elif (item_won == 'Special Item(Gold) Stat-Trak Well-Worn'):
            money_won += avg_stattrak_special[1]
        elif (item_won == 'Special Item(Gold) Stat-Trak Field-Tested'):
            money_won += avg_stattrak_special[2]
        elif (item_won == 'Special Item(Gold) Stat-Trak Minimal Wear'):
            money_won += avg_stattrak_special[3]
        else:
            money_won += avg_stattrak_special[4]
        print(money_won)
        return money_won
    
    # Function to updates the labels money spent, and gambler's fallacy.
    def label_updater(self, reset, unlock_reward):
        global money_spent
        global fallacy
        global unlock_count
        global wallet

        if (reset == True):
            money_list.clear()
            money_earned = sum(money_list)
            money_spent = 0.00
            fallacy = 0.00
            unlock_count = 0
            wallet = 0.00
            self.labelUnlockCount.configure(text_color='#FFFFFF', text="Unlock Count: #" + str(unlock_count))
            self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_earned))
            self.labelWallet.configure(text_color='#FFFFFF', text="Wallet: $ " + str(wallet))
        else:
            money_spent += 3.44
            money_spent = round(money_spent, 2)
            money_earned = sum(money_list)
            fallacy = round(fallacy, 5)
            fallacy = self.gambler_fallacy(fallacy, unlock_reward)
            unlock_count += 1
            wallet = money_earned - money_spent
            wallet = round(wallet, 2)
        
        self.labelUnlockCount.configure(text_color='#FFFFFF', text="Unlock Count: #" + str(unlock_count))
        self.labelFallacy.configure(text_color='#00d0ff', text="Fallacy: " + str(fallacy) + '%')
        self.labelMoneySpent.configure(text_color='red', text="Money Spent: $" + str(money_spent))
        self.labelWallet.configure(text_color='#FFFFFF', text="Wallet: $ " + str(wallet))
        
        
    # Function that will auto-unlock a user specified number of cases after auto unlock button is pressed.
    def auto_unlock(self):
        no_reset = False
        unlock_num = self.entry.get()
        unlock_num = int(unlock_num)
        item_money = 0.00
        for i in range(unlock_num):
            unlock_reward = self.case_unlock()
            self.label_updater(no_reset, unlock_reward)

            if ('Mil-Spec' in unlock_reward):
                item_money = self.money_mil_spec(unlock_reward)
                money_list.append(item_money)
                money_sum = sum(money_list)
                money_sum = round(money_sum, 2)
                self.textbox.insert("insert", unlock_reward + "\n")
                self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
            elif ('Restricted' in unlock_reward):
                item_money = self.money_restricted(unlock_reward)
                money_list.append(item_money)
                money_sum = sum(money_list)
                money_sum = round(money_sum, 2)
                self.textbox.insert("insert", unlock_reward + "\n")
                self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
            elif ('Classified' in unlock_reward):
                item_money = self.money_classified(unlock_reward)
                money_list.append(item_money)
                money_sum = sum(money_list)
                money_sum = round(money_sum, 2)
                self.textbox.insert("insert", unlock_reward + "\n")
                self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
            elif ('Covert' in unlock_reward):
                item_money = self.money_covert(unlock_reward)
                money_list.append(item_money)
                money_sum = sum(money_list)
                money_sum = round(money_sum, 2)
                self.textbox.insert("insert", unlock_reward + "\n")
                self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
            else:
                item_money = self.money_special(unlock_reward)
                money_list.append(item_money)
                money_sum = sum(money_list)
                money_sum = round(money_sum, 2)
                self.textbox.insert("insert", unlock_reward + "\n")
                self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
            self.textbox.see("end")

    # Function that executes after each unlock button press
    def button_callback(self):
        no_reset = False
        unlock_reward = self.case_unlock()
        item_money = 0.00
        if ('Mil-Spec' in unlock_reward):
            item_money = self.money_mil_spec(unlock_reward)
            money_list.append(item_money)
            money_sum = sum(money_list)
            money_sum = round(money_sum, 2)
            self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
        elif ('Restricted' in unlock_reward):
            item_money = self.money_restricted(unlock_reward)
            money_list.append(item_money)
            money_sum = sum(money_list)
            money_sum = round(money_sum, 2)
            self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
        elif ('Classified' in unlock_reward):
            item_money = self.money_classified(unlock_reward)
            money_list.append(item_money)
            money_sum = sum(money_list)
            money_sum = round(money_sum, 2)
            self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
        elif ('Covert' in unlock_reward):
            item_money = self.money_covert(unlock_reward)
            money_list.append(item_money)
            money_sum = sum(money_list)
            money_sum = round(money_sum, 2)
            self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
        else:
            item_money = self.money_special(unlock_reward)
            money_list.append(item_money)
            money_sum = sum(money_list)
            money_sum = round(money_sum, 2)
            self.labelMoneyEarned.configure(text_color='#05f709', text="Money Earned: $" + str(money_sum))
        self.textbox.insert("insert", unlock_reward + "\n")
        self.textbox.see("end")
        self.label_updater(no_reset, unlock_reward)

    # Function to reset the simulation.
    def reset_skinulator(self, unlock_reward):
        reset_sim = True
        self.label_updater(reset_sim, unlock_reward)
        self.textbox.delete('0.0', 'end')
    

if __name__ == "__main__":
    app = App()
    app.mainloop()