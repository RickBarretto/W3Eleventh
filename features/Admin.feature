Feature: Admin Management

    Scenario: Verifying Administrator
        Given I am some User
            And I am an Admin
        When I try to verify if I am an Admin
        Then the verification should pass

    Scenario: Verifying non-Administrator User
        Given I am some User
            But I am not an Admin
        When I try to verify if I am an Admin
        Then the verification should fail


    Scenario: Registering a New Admin
        Given I'm an Owner
            And I have some address
        When I register this new address as a new admin
        Then the new admin should be registered successfully

    Scenario: No Permission to Register
        Given I'm a Customer
            And I have some address
        When I try to register this new address as admin
        Then it should rollover "Must be EOA"

    Scenario: No Permission to Register (Admin)
        Given I'm an Administrator
            And I have some address
        When I try to register this new address as admin (Admin)
        Then it should rollover "Must be EOA" (Admin)


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
