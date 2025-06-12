#!/usr/bin/env python3
"""
Solana Vanity Wallet Generator Module

This module provides functionality to generate Solana wallets with custom prefixes or suffixes.
"""

from solana.keypair import Keypair
import base58
import time
from typing import Dict, Optional, Callable


class VanityWalletGenerator:
    """Generate Solana wallets with custom prefixes or suffixes."""
    
    def __init__(self):
        self.stop_flag = False
        self.attempts = 0
        self.start_time = None
        
    def stop(self):
        """Stop the generation process."""
        self.stop_flag = True
        
    def reset(self):
        """Reset the generator state."""
        self.stop_flag = False
        self.attempts = 0
        self.start_time = None
        
    def generate_vanity_wallet(
        self, 
        target: str, 
        case_sensitive: bool = False,
        progress_callback: Optional[Callable[[int, float], None]] = None
    ) -> Optional[Dict[str, str]]:
        """
        Generate a Solana wallet with a public key that starts or ends with the target phrase.
        
        Args:
            target: The target phrase to search for
            case_sensitive: Whether the search should be case sensitive
            progress_callback: Optional callback function that receives (attempts, elapsed_time)
            
        Returns:
            Dictionary with wallet details if found, None if stopped
        """
        self.reset()
        self.start_time = time.time()
        
        # Prepare target for comparison
        search_target = target if case_sensitive else target.lower()
        
        while not self.stop_flag:
            self.attempts += 1
            
            # Generate new keypair
            keypair = Keypair.generate()
            pubkey_str = str(keypair.public_key)
            
            # Prepare public key for comparison
            pubkey_compare = pubkey_str if case_sensitive else pubkey_str.lower()
            
            # Check for match
            is_prefix = pubkey_compare.startswith(search_target)
            is_suffix = pubkey_compare.endswith(search_target)
            
            if is_prefix or is_suffix:
                # Found a match!
                privkey_b58 = base58.b58encode(keypair.secret_key).decode()
                
                return {
                    "public_key": pubkey_str,
                    "private_key": privkey_b58,
                    "match_type": "prefix" if is_prefix else "suffix",
                    "attempts": self.attempts,
                    "elapsed_time": time.time() - self.start_time
                }
            
            # Call progress callback if provided
            if progress_callback and self.attempts % 1000 == 0:
                elapsed = time.time() - self.start_time
                progress_callback(self.attempts, elapsed)
        
        return None
    
    def estimate_time(self, target_length: int, is_prefix: bool = True) -> Dict[str, float]:
        """
        Estimate the time required to find a wallet with given target length.
        
        Args:
            target_length: Length of the target phrase
            is_prefix: Whether searching for prefix (True) or suffix (False)
            
        Returns:
            Dictionary with time estimates in seconds
        """
        # Base58 alphabet has 58 characters
        # Probability of match = 1 / (58^target_length)
        # Expected attempts = 58^target_length
        
        base58_chars = 58
        expected_attempts = base58_chars ** target_length
        
        # Estimate generation rate (varies by system)
        # Rough estimate: 10,000 - 50,000 keys/second on modern hardware
        min_rate = 10000
        max_rate = 50000
        avg_rate = 30000
        
        return {
            "expected_attempts": expected_attempts,
            "estimated_seconds_min": expected_attempts / max_rate,
            "estimated_seconds_avg": expected_attempts / avg_rate,
            "estimated_seconds_max": expected_attempts / min_rate,
        }


def main():
    """Example usage of the VanityWalletGenerator."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generator.py <target_phrase>")
        print("Example: python generator.py wife")
        sys.exit(1)
    
    target = sys.argv[1]
    generator = VanityWalletGenerator()
    
    # Estimate time
    estimate = generator.estimate_time(len(target))
    print(f"\nSearching for wallets with '{target}'...")
    print(f"Expected attempts: {estimate['expected_attempts']:,.0f}")
    print(f"Estimated time: {estimate['estimated_seconds_avg']:.2f} seconds\n")
    
    def progress_update(attempts, elapsed):
        rate = attempts / elapsed
        print(f"\rAttempts: {attempts:,} | Rate: {rate:,.0f} keys/sec | Time: {elapsed:.2f}s", end="")
    
    # Generate wallet
    result = generator.generate_vanity_wallet(target, progress_callback=progress_update)
    
    if result:
        print(f"\n\n✅ Found matching wallet after {result['attempts']:,} attempts!")
        print(f"Time taken: {result['elapsed_time']:.2f} seconds")
        print(f"\nPublic Key: {result['public_key']}")
        print(f"Private Key: {result['private_key']}")
        print(f"Match Type: {result['match_type']}")
    else:
        print("\n\nGeneration stopped.")


if __name__ == "__main__":
    main() 