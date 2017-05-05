package com.studio.tlfam.wat;

import android.app.Activity;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.hardware.GeomagneticField;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.Manifest;
import android.location.LocationManager;
import android.location.LocationListener;
import android.location.Location;
import android.content.Context;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.widget.ImageView;
import android.widget.TextView;

/**
 * Created by tanguy on 03/04/17.
 */


public class GeolocationActivity extends Activity {

    TextView myTextViewGeoloc = null, myTextViewGeoloc2 = null;
    ImageView myArrow = null;
    GeomagneticField geoField;
    SensorManager mSensorManager = null;
    Float heading;
    Integer i = 0;
    BitmapFactory.Options imgOptions;

    private void rotateArrow(float angle) {
        Matrix matrix = new Matrix();
        myArrow.setScaleType(ImageView.ScaleType.MATRIX);
        matrix.postRotate(angle, imgOptions.outWidth/2, imgOptions.outHeight/2);
        myArrow.setImageMatrix(matrix);
    }

    private class MyLocationListener implements LocationListener {
        @Override
        public void onLocationChanged(Location location) {
            if (location != null) {

                String newString = "Latitude : " + location.getLatitude();
                newString += " et Longitude : " + location.getLongitude();

                myTextViewGeoloc.setText(newString);

                Location secondPosition = new Location(location);
                secondPosition.setLatitude(49.015671);
                secondPosition.setLongitude(2.242576);

                float bearing = location.bearingTo(secondPosition);
                float distance = location.distanceTo(secondPosition);

                String newString2 = " Bearing : " + bearing + " et Distance : " + distance;

                geoField = new GeomagneticField(
                        Double.valueOf(location.getLatitude()).floatValue(),
                        Double.valueOf(location.getLongitude()).floatValue(),
                        Double.valueOf(location.getAltitude()).floatValue(),
                        System.currentTimeMillis()
                );
                newString2 += "\n First Heading : " + heading;

                heading += geoField.getDeclination();
//                heading = (bearing - heading) * -1;
//                heading = normalizeDegree(heading);

                newString2 += "\n Geo Declination : " + geoField.getDeclination();

                newString2 += "\n Final Heading : " + heading;

                myTextViewGeoloc2.setText(newString2);

                rotateArrow(heading);
            }
        }

        private float normalizeDegree(float value) {
            if (value >= 0.0f && value <= 180.0f) {
                return value;
            } else {
                return 180 + (180 + value);
            }
        }

        @Override
        public void onProviderDisabled(String provider) {
        }

        @Override
        public void onProviderEnabled(String provider) {
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
        }
    }

    private class MySensorListener implements SensorEventListener {

        SensorManager sm = (SensorManager) getSystemService(SENSOR_SERVICE);

        public void start(){
            sm.registerListener(this, sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER),
                    SensorManager.SENSOR_DELAY_GAME);

            sm.registerListener(this, sm.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD),
                    SensorManager.SENSOR_DELAY_GAME);
        }

        @Override
        public void onSensorChanged(SensorEvent event) {
            // get the angle around the z-axis rotated
            heading = event.values[0];
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
            // not in use
        }
    }

    public static android.graphics.BitmapFactory.Options getSize(Context c, int resId){
        android.graphics.BitmapFactory.Options o = new android.graphics.BitmapFactory.Options();
        o.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(c.getResources(), resId, o);
        return o;
    }

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.geoloc_layout);

        myTextViewGeoloc = (TextView) findViewById(R.id.geolocLabel);
        myTextViewGeoloc2 = (TextView) findViewById(R.id.textView3);
        myArrow = (ImageView) findViewById(R.id.arrowDir);

        myArrow.setImageResource(R.mipmap.test);
        imgOptions = getSize(this, R.mipmap.test);

        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        LocationListener ll = new MyLocationListener();

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            myTextViewGeoloc.setText("User not allowed to get the position");

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    4);
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {

            myTextViewGeoloc.setText("User not allowed to get the position");

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                    4);
        }

        lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, ll);
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, ll);

        MySensorListener sl = new MySensorListener();
        sl.start();
    }

}
