Feature: Admin Management

    Scenario: Registering a New Admin
        Given I am an Admin
            And I have some address
        When I register this new address as a new admin
        Then the new admin should be registered successfully

    Scenario: No Permission to Register
        Given I am not an Admin
            And I have some address
        When I try to register this new address as admin
        Then it should rollover "Insufficient permission"


    Scenario: Listing All Admins
        Given I am an Admin 
            And there are multiple admins registered
        When I list all admins
        Then I should see the list of all registered admins

    Scenario: No Permission to Listing
        Given I am not an Admin
            And there are multiple admins registered
        When I request a list of admins
        Then it should rollover "Insufficient permission"


    Scenario: Verifying Admin Privileges
        Given I am a user
        When I try to access admin functionalities
        Then the admin privileges should be verified for me
