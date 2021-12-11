Insert INTO Users VALUES
    ('organizer1@gmail.com', 'org1', 'sampleUser1'),
    ('organizer2@gmail.com', 'org2', 'sampleUser2'),
    ('organizer3@gmail.com', 'org3', 'sampleUser3');

INSERT INTO Events VALUES
    ('1', 
     '2022 career fair', 
     'organizer1@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2022-11-15 12:10', 
     '2022-11-15 14:00',
     200
    ), 

    ('2', 
     '2022 student fair', 
     'organizer2@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2022-11-16 12:10', 
     '2022-11-16 14:00',
     200
    ), 

    ('3', 
     '2022 research fair', 
     'organizer3@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2022-11-17 12:10', 
     '2022-11-17 14:00',
     200
    ),

    ('4', 
     '2023 career fair', 
     'organizer1@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2023-11-15 12:10', 
     '2023-11-15 14:00',
     200
    ), 

    ('5', 
     '2024 career fair', 
     'organizer1@gmail.com', 
     'description', 
     ROW('columbia', 40.80778821286171, -73.96345656010647, 'address'),
     '2024-11-15 12:10', 
     '2024-11-15 14:00',
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
