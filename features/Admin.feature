Feature: Admin Management

    Scenario: Verifying Administrator
        Given I am some User
            And I am an Admin
        When I try to verify if I am an Admin¹
        Then the verification should pass

    Scenario: Verifying non-Administrator User
        Given I am some User
            But I am not an Administrator
        When I try to verify if I am an Administrator²
        Then the verification should fail


    Scenario: Successfully Registering a New Admin
        Given I'm an Owner
            And I have a Candidate
        When I try to register Candidate as a new admin¹
        Then the new admin should be registered successfully

    Scenario: Owner Trying to Register Existing Admin
        Given I'm an Owner
            And an Administrator
        When I try to re-register this Administrator
        Then it should rollover "Already admin"

    Scenario: Customer Trying to Register New Admin
        Given I'm a Customer
            And I have a Candidate
        When I try to register Candidate as a new admin²
        Then it should rollover "Must be EOA"¹

    Scenario: Admin Trying to Register New Admin
        Given I'm an Administrator
            And I have a Candidate
        When I try to register Candidate as a new admin³
        Then it should rollover "Must be EOA"²


    Scenario: Listing All Admins
        Given I am an Administrator
            And there are multiple administrators registered
        When I try to list all administrators¹
        Then I should see the list of all registered administrators

    Scenario: No Permission to Listing
        Given I am not an Administrator
            And there are multiple administrators registered
        When I try to list all administrators²
        Then it should rollover "Must be Admin"
