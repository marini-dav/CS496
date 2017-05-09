package com.example.sammy.cs496_androidui;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button verticalView = (Button) findViewById(R.id.button1);
        verticalView.setOnClickListener(new View.OnClickListener(){
           @Override
            public void onClick(View v) {
               Intent intent = new Intent(MainActivity.this, VerticalViewActivity.class);
               startActivity(intent);
           }
        });

        Button horizontalView = (Button) findViewById(R.id.button2);
        horizontalView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, HorizontalViewActivity.class);
                startActivity(intent);
            }
        });

        Button gridView = (Button) findViewById(R.id.button3);
        gridView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, GridViewActivity.class);
                startActivity(intent);
            }
        });

        Button relativeView = (Button) findViewById(R.id.button4);
        relativeView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, ListViewActivity.class);
                startActivity(intent);
            }
        });
    }
}
