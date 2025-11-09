#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod trade {
    use ink::storage::Mapping;

    #[derive(scale::Encode, scale::Decode, Clone, Debug, PartialEq, Eq)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub struct Card {
        pub name: String,
        pub power: u32,
    }

    #[derive(scale::Encode, scale::Decode, Clone, Debug, PartialEq, Eq)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub struct Proposal {
        pub card: Card,
        pub by: AccountId,
        pub to: AccountId,
    }

    #[derive(scale::Encode, scale::Decode, Clone, Debug, PartialEq, Eq)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub struct Auction {
        pub card: Card,
        pub proposals: Vec<Proposal>,
    }

    #[ink(storage)]
    pub struct TradeStore {
        auctions: Mapping<AccountId, Auction>,
    }

    impl TradeStore {
        #[ink(constructor)]
        pub fn new() -> Self {
            Self {
                auctions: Mapping::default(),
            }
        }

        #[ink(message)]
        pub fn expose(&mut self, card: Card) {
            let caller = self.env().caller();
            if self.auctions.get(&caller).is_none() {
                let auction = Auction {
                    card,
                    proposals: Vec::new(),
                };
                self.auctions.insert(caller, &auction);
            }
        }

        #[ink(message)]
        pub fn propose(&mut self, card: Card, to: AccountId) {
            let caller = self.env().caller();
            if let Some(mut auction) = self.auctions.get(&to) {
                let proposal = Proposal {
                    card,
                    by: caller,
                    to,
                };
                auction.proposals.push(proposal);
                self.auctions.insert(to, &auction);
            }
        }

        #[ink(message)]
        pub fn accept(&mut self, index: u32) {
            let caller = self.env().caller();
            if let Some(mut auction) = self.auctions.get(&caller) {
                if (index as usize) < auction.proposals.len() {
                    let proposal = auction.proposals.remove(index as usize);
                    // Swap cards between caller and proposer
                    self.auctions.insert(proposal.by, &Auction {
                        card: auction.card.clone(),
                        proposals: Vec::new(),
                    });
                    auction.card = proposal.card;
                    auction.proposals.clear();
                    self.auctions.insert(caller, &auction);
                }
            }
        }

        #[ink(message)]
        pub fn get_auction(&self, owner: AccountId) -> Option<Auction> {
            self.auctions.get(&owner)
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use ink::env::test;

        fn set_caller(caller: AccountId) {
            test::set_caller::<Environment>(caller);
        }

        #[ink::test]
        fn expose_and_propose_works() {
            let mut store = TradeStore::new();
            let accounts = test::default_accounts::<Environment>();
            
            set_caller(accounts.alice);
            store.expose(Card { name: "Dragon".into(), power: 100 });

            set_caller(accounts.bob);
            store.propose(Card { name: "Goblin".into(), power: 30 }, accounts.alice);

            let auction = store.get_auction(accounts.alice).unwrap();
            assert_eq!(auction.proposals.len(), 1);
            assert_eq!(auction.proposals[0].card.name, "Goblin");
        }

        #[ink::test]
        fn accept_proposal_works() {
            let mut store = TradeStore::new();
            let accounts = test::default_accounts::<Environment>();

            set_caller(accounts.alice);
            store.expose(Card { name: "Dragon".into(), power: 100 });

            set_caller(accounts.bob);
            store.propose(Card { name: "Goblin".into(), power: 30 }, accounts.alice);

            set_caller(accounts.alice);
            store.accept(0);

            let alice_auction = store.get_auction(accounts.alice).unwrap();
            let bob_auction = store.get_auction(accounts.bob).unwrap();

            assert_eq!(alice_auction.card.name, "Goblin");
            assert_eq!(bob_auction.card.name, "Dragon");
        }
    }
}
