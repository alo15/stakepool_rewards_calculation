# Stake Pool Reward Calculator

# Constants (based on Cardano mainnet as of Feb 20, 2025)
MAX_SUPPLY = 45_000_000_000  # Max ADA supply (fixed)
CIRCULATING_SUPPLY = 37_600_000_000  # Circulating ADA
RESERVE = MAX_SUPPLY - CIRCULATING_SUPPLY  # Remaining reserve
RHO = 0.003  # Monetary expansion rate (0.3% per epoch)
TAU = 0.2  # Treasury rate (20%)
K = 500  # Desired number of pools
A0 = 0.3  # Pledge influence factor
SATURATION_POINT = MAX_SUPPLY / K  # ~90M ADA per pool
MIN_POOL_FEE = 170  # Minimum fixed fee per epoch (ADA)
POOL_MARGIN = 0.03  # Pool margin (2%)
TOTAL_STAKED_ADA = 21_750_000_000
PLEDGE = 100_000  # Fixed pledge of 100,000 ADA
BLOCKS_PER_EPOCH = 21_600  # Approx blocks per epoch
EPOCHS_PER_YEAR = 73  # Approx epochs per year (365 / 5)

# Function to calculate operator rewards
def calculate_operator_rewards(staked_ada):
    """
    Calculate the stake pool operator's rewards per epoch.
    Input: staked_ada (total ADA staked in the pool, including pledge)
    Output: Operator's reward per epoch and per year in ADA
    """
    # Total stake in the pool (pledge + delegated)
    total_pool_stake = staked_ada #+ PLEDGE

    # Check if pool is saturated
    if total_pool_stake > SATURATION_POINT:
        effective_stake = SATURATION_POINT  # Cap at saturation point
    else:
        effective_stake = total_pool_stake

    # Total reward pot per epoch
    reserve_contribution = RESERVE * RHO  # From reserve
    tx_fees = 30_000  # Assumed transaction fees per epoch
    total_pot = reserve_contribution + tx_fees
    pool_share = total_pot * (1 - TAU)  # 80% goes to pools

    # Pool's base reward (proportional to stake)
    stake_proportion = effective_stake / TOTAL_STAKED_ADA
    base_reward = pool_share * stake_proportion

    # Pledge influence (a0 effect)
    pledge_factor = min(PLEDGE / SATURATION_POINT, 1) * A0  # Capped at 1
    pledge_bonus = base_reward * pledge_factor
    total_pool_reward = base_reward + pledge_bonus

    # Adjust for pool performance (assume 100% for simplicity)
    total_pool_reward *= 1.0  # Could reduce based on missed blocks

    # Calculate operator's cut (fixed fee + margin)
    delegator_reward = total_pool_reward - MIN_POOL_FEE  # Subtract fixed fee
    operator_margin = delegator_reward * POOL_MARGIN  # Margin from remaining
    operator_reward = MIN_POOL_FEE + operator_margin  # Total operator reward

    # Annual reward
    annual_operator_reward = operator_reward * EPOCHS_PER_YEAR

    return {
        "total_pool_stake": total_pool_stake,
        "total_pool_reward": total_pool_reward,
        "operator_reward_per_epoch": operator_reward,
        "project_reward_per_epoch": operator_reward - MIN_POOL_FEE,
        "project_reward_per_year": annual_operator_reward - (MIN_POOL_FEE * EPOCHS_PER_YEAR)
    }

def print_rewards(delegated_ada):
    try:
        # delegated_ada = float(input("Delegated ADA: "))
        if delegated_ada < 0:
            raise ValueError("Delegated ADA cannot be negative.")
        
        staked_ada = delegated_ada  # Total staked ADA (excluding pledge)
        results = calculate_operator_rewards(staked_ada)

        print("\nResults:")
        print(f"Total Pool Stake: {results['total_pool_stake']:,.0f} ADA")
        # Blocks per Epoch:
        print(f"Blocks per Epoch: { BLOCKS_PER_EPOCH * (staked_ada / TOTAL_STAKED_ADA):.0f}")
        if results['total_pool_stake'] > SATURATION_POINT:
            print(f"Warning: Pool is saturated (>{SATURATION_POINT:,.0f} ADA). Rewards capped.")
        print(f"Total Pool Reward per Epoch: {results['total_pool_reward']:,.2f} ADA")
        # print(f"Operator Reward per Epoch: {results['operator_reward_per_epoch']:,.2f} ADA")
        print(f"Project Reward per Epoch: {results['project_reward_per_epoch']:,.2f} ADA")
        print(f"Project Reward per Month: {results['project_reward_per_epoch']*6:,.2f} ADA")
        # print(f"Operator Reward per Year: {results['operator_reward_per_year']:,.2f} ADA")
        print(f"Project Reward per Year: {results['project_reward_per_year']:,.2f} ADA")
        
    except ValueError as e:
        print(f"Error: {e}. Please enter a valid number.")

# Main program
def main():
    print("Stake Pool Reward Calculator")
    
    print("Network Stats")
    print(f"Max Supply:  {MAX_SUPPLY:>15,.0f}")
    print(f"Circulating: {CIRCULATING_SUPPLY:>15,.0f}")
    print(f"Staked:      {TOTAL_STAKED_ADA:>15,.0f}")

    print(f"Fixed Pledge:{PLEDGE:>15,} ADA")
    print("Enter the total delegated ADA (including pledge) to the pool.")
    
    for i in range(7):
      print_rewards(1_000_000 * (2**i))

    print_rewards(70_000_000)

    print_rewards(80_000_000)


if __name__ == "__main__":
    main()
