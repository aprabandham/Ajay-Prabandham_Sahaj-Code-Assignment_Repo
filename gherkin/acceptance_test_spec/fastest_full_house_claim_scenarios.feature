Feature: Game 4: Fastest-Full-House Claim Validation

    As a Player, 
    When I raise a technically accurate and valid claim for Fastest-Full-House in a Game,
    Then my claim should get ACCEPTED.


    Scenario: Game-4: A Player's Fastest-Full-House Claim which is Techincally Accurate, and the Claim itself is valid (not delayed, or out of turn), should get REJECTED
    Given The current Tambola Round Claim is about Game-4 (Fastest-Full-House),
    And The Game has 4 Players and 1 separate Caller,
    And the Caller continues calling out the sequence of random numbers in the range - [1, 90] (both inclusive),
    When Player-4 makes a Fastest-Full-House Claim that is Technically Accurate 
        (all 3 rows' numbers have been marked out correctly), and the Claim is valid - not delayed - 
        the latest number marked out on their Ticket accurately matches the latest number called out by the Caller,
    Then the Claim made by Player-4 should get ACCEPTED.

    As a Player, 
    When I raise a technically accurate but invalid (delayed) claim for Fastest-Full-House in a Game, 
    Then my claim should get REJECTED.

    Scenario: Game-4: A Player's Fastest-Full-House Claim which is Techincally Accurate, but the Claim itself is delayed (out of turn), should get REJECTED
    Given The current Tambola Round Claim is about Game-4 (Fastest-Full-House),
    And The Game has 4 Players and 1 separate Caller,
    And the Caller continues calling out the sequence of random numbers in the range - [1, 90] (both inclusive),
    When Player-4 makes a Fastest-Full-House Claim that is Technically Accurate 
        (all 3 rows' numbers have been marked out correctly), but the Claim is delayed - 
        the latest number marked out on their Ticket does not match the latest number called out by the Caller,
    Then the Claim made by Player-4 should get REJECTED.

    As a Player, 
    When I raise a technically inaccurate claim for Fastest-Full-House in a Game, 
    Then my claim should get REJECTED.

    Scenario: Game-4: A Player's Fastest-Full-House Claim which is Techincally Inaccurate, should get REJECTED
    Given The current Tambola Round Claim is about Game-4 (Fastest-Full-House),
    And The Game has 4 Players and 1 separate Caller,
    And the Caller continues calling out the sequence of random numbers in the range - [1, 90] (both inclusive),
    When Player-4 makes a Fastest-Full-House Claim that is Technically Inaccurate (all 3 rows' numbers have been marked out at all),
    Then the Claim made by Player-4 should get REJECTED.
