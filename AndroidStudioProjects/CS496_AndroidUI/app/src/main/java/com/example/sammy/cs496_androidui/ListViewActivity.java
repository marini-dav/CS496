package com.example.sammy.cs496_androidui;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import java.util.ArrayList;

public class ListViewActivity extends AppCompatActivity {
    private ArrayList<Integer> numbers = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity4);

        for(int i = 1; i<=5; i++) {
            numbers.add(i);
        }

        ListView listView = (ListView) findViewById(R.id.list_view_id);

        //ArrayAdapter adapter = new ArrayAdapter(this, R.layout.activity4, numbers);
        final ListAdapter adapter = new ArrayAdapter(this, R.layout.activity4, numbers);
        listView.setAdapter(adapter);
    }
}