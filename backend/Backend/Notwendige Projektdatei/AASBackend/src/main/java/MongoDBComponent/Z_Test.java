package MongoDBComponent;

import java.time.LocalDateTime;
import java.util.Calendar;
import java.util.Date;
import java.util.Random;

public class Z_Test {

	public static final String mongoDbPassword = "3rNSZmxIte1bTHeN"; 
	public static final String mongoDbConnectionString = "mongodb+srv://bkaemper:" + mongoDbPassword + "@cluster0.zgwztqy.mongodb.net/"; // Ihre MongoDB-Verbindungszeichenfolge hier
	public static final String customerId = "10001"; 

	public static void main(String[] args) {
		System.out.println("test");
		MongoDbConnector connector = new MongoDbConnector(mongoDbConnectionString);
		MongoDbTsHandler tsHandler = new MongoDbTsHandler(connector);


		String[] smePaths = new String[10];
		for (int i = 0; i < smePaths.length; i++) {
			smePaths[i] = "MeasuredValueFlowTemperature/PresentValue";
		}
		
		
		Object[] values = new Object[10];
		for (int i = 0; i < values.length; i++) {
			values[i] = generateRandomDoubleInRange(45,48);
		}
		for (int i = 0; i < values.length; i++) {
			System.out.println(values[i]);
		}

		Date startDate = new Date(2024-1900, 0, 1, 0, 5); // Beachten Sie: Monate sind 0-basiert
		
		Date[] dates = new Date[10];
		dates[0] = startDate;
		for (int i = 1; i < dates.length; i++) {
			dates[i] = addMinutes(dates[i-1], 5);
		}
		for (int i = 0; i < dates.length; i++) {
			System.out.println(dates[i]);
		}

		tsHandler.insertManyEntries(
				customerId,
				"th-koeln.de/gart/aas/1706097216425",
				"OperatingInformation", 
				smePaths, 
				dates, 
				values);


		System.out.println("test done");
	}

	public static double generateRandomDoubleInRange(double min, double max) {
		if (min >= max) {
			throw new IllegalArgumentException("Maximalwert muss größer als Minimalwert sein");
		}

		Random random = new Random();
		return min + (max - min) * random.nextDouble();
	}

	public static Date addMinutes(Date date, int minutesToAdd) {
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        calendar.add(Calendar.MINUTE, minutesToAdd);
        return calendar.getTime();
    }



}
