cardata = hdf5read('1537377117.hdf5','carcount');
timedata = hdf5read('1537377117.hdf5','time');

%index through the time stamps and convert from epoch to regular time
%subtract 14,400 seconds to account for GMT being 4 hours ahead
for i=1:length(timedata)
    time(i) = datetime(timedata(i)-14400,'ConvertFrom','posixtime');
end

time = time';

bar(time,cardata)
title('Number of Cars Detected per Frame')
xlabel('Time')
ylabel('Number of Cars Detected')

for i = 2:(length(cardata))
    cardata(i) = cardata(i) + cardata(i-1);
end

figure 

bar(time,cardata)
title('Running Sum of Cars Detected per Frame')
xlabel('Time')
ylabel('Running Number of Cars Detected')
