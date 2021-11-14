Insert INTO Users VALUES
    ('organizer1@gmail.com', '1', 'sample user1'),
    ('organizer2@gmail.com', '2', 'sample user2'),
    ('organizer3@gmail.com', '3', 'sample user3');

INSERT INTO Events VALUES
    ('1', 
     '2021 career fair', 
     'organizer1@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2021-11-15 12:10', 
     '2021-11-15 14:00',
     200
    ), 

    ('2', 
     '2021 student fair', 
     'organizer2@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2021-11-16 12:10', 
     '2021-11-16 14:00',
     200
    ), 

    ('3', 
     '2021 research fair', 
     'organizer3@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2021-11-17 12:10', 
     '2021-11-17 14:00',
     200
    ),

    ('4', 
     '2020 career fair', 
     'organizer1@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2020-11-15 12:10', 
     '2020-11-15 14:00',
     200
    ), 

    ('5', 
     '2022 career fair', 
     'organizer1@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2022-11-15 12:10', 
     '2022-11-15 14:00',
     200
    );

INSERT INTO Attendance VALUES
    ('1', 'invite1@gmail.com', 'attendee', 'pc1'), 
    ('1', 'invite2@gmail.com', 'attendee', 'pc2'),
    ('1', 'invite3@gmail.com', 'attendee', 'pc3'),
    ('2', 'invite1@gmail.com', 'attendee', 'pc1'), 
    ('2', 'invite2@gmail.com', 'attendee', 'pc2'),
    ('2', 'invite3@gmail.com', 'attendee', 'pc3'),
    ('3', 'invite1@gmail.com', 'attendee', 'pc1'), 
    ('3', 'invite2@gmail.com', 'attendee', 'pc2'),
    ('3', 'invite3@gmail.com', 'attendee', 'pc3');
