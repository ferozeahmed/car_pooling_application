Scenario: Register a user
    Given I am on the register page
    When I fill in the following:
        | First Name | user |
        | Last Name  | one  |
        | Email      | user_one@comcast.comcast |
        | mobile     | 1234567890 |
        | address    | abc, pallavaram, chennai 600117 |
        | vehicle   | car |
        | Seats Offered   | 4 |
    And I press "Register"
    Then I should see "Welcome! You have signed up successfully."


Scenario: Login as user and offer a ride to office
    Given I am on the login page
    When I fill in the following:
        | Email      | user_one@comcast.com |
    And I press "Login"
    Then I should see "Signed in successfully."
    When I click on "Offer a ride"
    And I fill in the following:
        | Destination | office |
        | Date | 2024-05-30 |
        | Time | 80:00 AM |
    And I press "Offer"
    Then I should see "Ride offered successfully."


Scenario: Login as user and search for a ride to office and accept ride
    Given I am on the login page
    When I fill in the following:
        | Email      | user_two@comcast.com |
    And I press "Login"
    Then I should see "Signed in successfully."
    When I click on "Search a ride"
    And I fill in the following:
        | Destination | office |
        | Date | 2024-05-30 |
        | Time | 80:00 AM |
    And I press "Search"
    Then I should see "Ride found successfully."
    When I click on "Accept"
    Then I should see "Ride accepted successfully."
    And I should see "Ride details"


Scenario: Login as user and view details of the offered ride
    Given I am on the login page
    When I fill in the following:
        | Email      | user_one@comcast.com |
    And I press "Login"
    Then I should see "Signed in successfully."
    When I click on "View offered ride"
    Then I should see "Ride details"
    And I should see "user_two"


Scenario: Login as user and view details of the accepted ride
    Given I am on the login page
    When I fill in the following:
        | Email      | user_two@comcast.com |
    And I press "Login"
    Then I should see "Signed in successfully."
    When I click on "View accepted ride"
    Then I should see "Ride details"
    And I should see "user_one"


Scenario: Login as user and complete the ride
    Given I am on the login page
    When I fill in the following:
        | Email      |  user_one@comcast.com
    And I press "Login"
    Then I should see "Signed in successfully."
    When I click on "Complete ride"
    Then I should see "Ride completed successfully."
