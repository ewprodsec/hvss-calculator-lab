from hvss_common import calc_exploitability, calc_xcia, calc_xps, calc_xsd, calc_xhb

def get_input(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

print("Welcome to HVSS ML CLI")

av_value = get_input("Enter Attack Vector (AV) :\n[1] Network (N)\n[2] Adjacent (A)\n[3] Local (L)\n[4] Physical (P)\n", 1, 4)
eac_value = get_input("Enter Extended Attack Complexity (EAC) :\n[1] Negligible (N)\n[2] Low (L)\n[3] Medium (M)\n[4] High (H)\n[5] Critical (C)\n[6] Extreme (E)\n", 1, 6)
pr_value = get_input("Enter Privileges Required (PR) :\n[1] None (N)\n[2] Low (L)\n[3] High (H)\n", 1, 3)
ui_value = get_input("Enter User Interaction (UI) :\n[1] None (N)\n[2] Required (R)\n", 1, 2)
xit_value = get_input("Enter Impact Type (XIT):\n[1] Original CIA (XCIA)\n[2] Patient Safety (XPS)\n[3] Sensitive Data (XSD)\n[4] Hospital Breach (XHB)\n", 1, 5)

if xit_value == 1:
    xcia_c_value = get_input("Enter Confidentiality (C):\n[1] None (N)\n[2] Low (L)\n[3] High (H)\n", 1, 3)
    xcia_i_value = get_input("Enter Integrity (I):\n[1] None (N)\n[2] Low (L)\n[3] High (H)\n", 1, 3)
    xcia_a_value = get_input("Enter Availability (A):\n[1] None (N)\n[2] Low (L)\n[3] High (H)\n", 1, 3)
    prediction = calc_xcia([av_value, eac_value, pr_value, ui_value, xcia_c_value, xcia_i_value, xcia_a_value])
    prediction_exploitability = calc_exploitability([av_value, eac_value, pr_value, ui_value])
    print(f"Exploitability: {prediction_exploitability}")
    print(f"Final XCIA: {prediction}")
elif xit_value == 2:
    xps_value = get_input("Enter Patient Safety (XPS):\n[1] Negligible (N)\n[2] Limited (L)\n[3] Moderate (MD)\n[4] Major (MJ)\n[5] Critical (C)\n", 1, 5)
    prediction = calc_xps([av_value, eac_value, pr_value, ui_value, xps_value])
    prediction_exploitability = calc_exploitability([av_value, eac_value, pr_value, ui_value])
    print(f"Exploitability: {prediction_exploitability}")
    print(f"Final XPS: {prediction}")
elif xit_value == 3:
    xsd_value = get_input("Enter Sensitive Data (XSD):\n[1] None (N)\n[2] Secondary Personal Identifiers is less than 10,000 (SL)\n[3] Secondary Personal Identifiers is greater than 10,000 (SG)\n[4] Primary Personal Identifiers is less than 10,000 (PL)\n[5] Primary Personal Identifiers is greater than 10,000 (PG)\n", 1, 5)
    prediction = calc_xsd([av_value, eac_value, pr_value, ui_value, xsd_value])
    prediction_exploitability = calc_exploitability([av_value, eac_value, pr_value, ui_value])
    print(f"Exploitability: {prediction_exploitability}")
    print(f"Final XSD: {prediction}")
elif xit_value == 4:
    xhb_value = get_input("Enter Hospital Breach (XH1B):\n[1] None (N)\n[2] Device Availability (DA)\n[3] Network Access (NA)\n[4] User Impersonation (UI)\n", 1, 4)
    prediction = calc_xhb([av_value, eac_value, pr_value, ui_value, xhb_value])
    prediction_exploitability = calc_exploitability([av_value, eac_value, pr_value, ui_value])
    print(f"Exploitability: {prediction_exploitability}")
    print(f"Final XHB: {prediction}")