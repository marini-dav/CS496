package com.example.sammy.cs496_sqlite_location;

import android.content.DialogInterface;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteDatabase;
import android.location.Location;
import android.provider.BaseColumns;
import android.support.v4.widget.SimpleCursorAdapter;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.database.Cursor;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.EditText;
import android.content.ContentValues;
import android.util.Log;
import android.Manifest;
import android.app.Dialog;
import android.content.pm.PackageManager;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;

import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

public class MainActivity extends AppCompatActivity implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener {
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private String mLatText;
    private String mLongText;
    private Location mLastLocation;
    private LocationListener mLocationListener;
    private static final int LOCATION_PERMISSION_RESULT = 17;
    SQLiteExample mSQLiteExample;
    Button mSQLSubmitButton;
    Cursor mSQLCursor;

    SimpleCursorAdapter mSQLCursorAdapter;
    private static final String TAG = "SQLActivity";
    SQLiteDatabase mSQLDB;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mLatText = "44.5";
        mLongText = "-123.2";

        if (mGoogleApiClient == null) {
            mGoogleApiClient = new GoogleApiClient.Builder(this)
                    .addConnectionCallbacks(this)
                    .addOnConnectionFailedListener(this)
                    .addApi(LocationServices.API)
                    .build();
        }
        mLocationRequest = LocationRequest.create();
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        mLocationRequest.setInterval(5000);
        mLocationRequest.setFastestInterval(5000);
        mLocationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location){
                if (location != null) {
                    mLatText = String.valueOf(location.getLatitude());
                    mLongText = String.valueOf(location.getLongitude());
                } else {
                    AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                    builder.setMessage(R.string.location_fail).setTitle(R.string.failure);
                    builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int id) {
                            // Do nothing
                        }
                    });
                    AlertDialog dialog = builder.create();
                    dialog.show();
                }
            }
        };

        mSQLiteExample = new SQLiteExample(this);
        mSQLDB = mSQLiteExample.getWritableDatabase();

        mSQLSubmitButton = (Button) findViewById(R.id.addButton);
        mSQLSubmitButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                if(mSQLDB !=null) {
                    EditText editText = (EditText) findViewById(R.id.editText);
                    String textBoxContents = editText.getText().toString();
                    editText.setText("");

                    ContentValues vals = new ContentValues();
                    vals.put(DBContract.DemoTable.COLUMN_NAME_NOTE, textBoxContents);
                    vals.put(DBContract.DemoTable.COLUMN_NAME_LAT, mLatText);
                    vals.put(DBContract.DemoTable.COLUMN_NAME_LONG, mLongText);
                    mSQLDB.insert(DBContract.DemoTable.TABLE_NAME, null, vals);

                    populateTable();
                } else {
                    Log.d(TAG, "Unable to access database for writing.");
                }
            }
        });
        populateTable();
    }
    @Override
    protected void onStart() {
        mGoogleApiClient.connect();
        super.onStart();
    }
    @Override
    protected void onStop() {
        mGoogleApiClient.disconnect();
        super.onStop();
    }
    @Override
    public void onConnected(@Nullable Bundle bundle){
        if(ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_DENIED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_DENIED){
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, LOCATION_PERMISSION_RESULT);
            return;
        }
        updateLocation();
    }
    @Override
    public void onConnectionSuspended(int i){

    }
    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult){
        Dialog errDialog = GoogleApiAvailability.getInstance().getErrorDialog(this, connectionResult.getErrorCode(), 0);
        errDialog.show();
        return;
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults){
        if(requestCode == LOCATION_PERMISSION_RESULT){
            if(grantResults.length > 0){
                updateLocation();
            } else {
                mLatText = "44.5";
                mLongText = "-123.2";
            }
        }
    }

    private void updateLocation(){
        if(ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_DENIED) {
            return;
        }
        LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, mLocationListener);
        mLastLocation = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
        if(mLastLocation != null) {
            mLatText = String.valueOf(mLastLocation.getLatitude());
            mLongText = String.valueOf(mLastLocation.getLongitude());
        } else {
            LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, mLocationListener);
        }
    }

    private void populateTable(){
        if(mSQLDB != null){
            try {
                if(mSQLCursorAdapter != null && mSQLCursorAdapter.getCursor() != null){
                    if(!mSQLCursorAdapter.getCursor().isClosed()){
                        mSQLCursorAdapter.getCursor().close();
                    }
                }
                mSQLCursor = mSQLDB.query(DBContract.DemoTable.TABLE_NAME,
                        new String[]{DBContract.DemoTable._ID, DBContract.DemoTable.COLUMN_NAME_NOTE,
                                DBContract.DemoTable.COLUMN_NAME_LAT, DBContract.DemoTable.COLUMN_NAME_LONG},
                        null, null, null, null, null);

                ListView SQLListView = (ListView) findViewById(R.id.listView);

                mSQLCursorAdapter = new SimpleCursorAdapter(this,
                        R.layout.sql_item,
                        mSQLCursor,
                        new String[]{DBContract.DemoTable.COLUMN_NAME_NOTE, DBContract.DemoTable.COLUMN_NAME_LAT, DBContract.DemoTable.COLUMN_NAME_LONG},
                        new int[]{R.id.sql_listview_note, R.id.sql_listview_lat, R.id.sql_listview_long},
                        0);
                SQLListView.setAdapter(mSQLCursorAdapter);

            } catch (Exception e) {
                Log.d(TAG, "Error loading data from database");
            }
        }
    }
}

class SQLiteExample extends SQLiteOpenHelper {

    public SQLiteExample(Context context) {
        super(context, DBContract.DemoTable.DB_NAME, null, DBContract.DemoTable.DB_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db){
        db.execSQL(DBContract.DemoTable.SQL_CREATE_DEMO_TABLE);

        ContentValues testValues = new ContentValues();
        testValues.put(DBContract.DemoTable.COLUMN_NAME_NOTE, "Notes");
        testValues.put(DBContract.DemoTable.COLUMN_NAME_LAT, "Latitude");
        testValues.put(DBContract.DemoTable.COLUMN_NAME_LONG, "Longitude");
        db.insert(DBContract.DemoTable.TABLE_NAME, null, testValues);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion){
        db.execSQL(DBContract.DemoTable.SQL_DROP_DEMO_TABLE);
        onCreate(db);
    }
}

final class DBContract {
    private DBContract(){};

    public final class DemoTable implements BaseColumns {
        public static final String DB_NAME = "notes_lat_long";
        public static final String TABLE_NAME = "Main";
        public static final String COLUMN_NAME_NOTE = "Notes";
        public static final String COLUMN_NAME_LAT = "Latitude";
        public static final String COLUMN_NAME_LONG = "Longitude";
        public static final int DB_VERSION = 1;

        public static final String SQL_CREATE_DEMO_TABLE = "CREATE TABLE " +
                DemoTable.TABLE_NAME + "(" + DemoTable._ID + " INTEGER PRIMARY KEY NOT NULL," +
                DemoTable.COLUMN_NAME_NOTE + " VARCHAR(255)," +
                DemoTable.COLUMN_NAME_LAT + " VARCHAR(255)," +
                DemoTable.COLUMN_NAME_LONG + " VARCHAR(255));";

        public  static final String SQL_DROP_DEMO_TABLE = "DROP TABLE IF EXISTS " + DemoTable.TABLE_NAME;
    }
}