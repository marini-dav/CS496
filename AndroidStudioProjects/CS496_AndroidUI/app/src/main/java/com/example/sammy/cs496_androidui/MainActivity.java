package com.example.sammy.cs496_androidui;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView hView = (TextView) findViewById(R.id.textView1);
        hView.setOnClickListener(new View.OnClickListener(){
           @Override
            public void onClick(View v){
               Intent intent = new Intent(MainActivity.this, HorizontalViewActivity.class);
               startActivity(intent);
           }
        });
        TextView vView = (TextView) findViewById(R.id.textView2);
        vView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, VerticalViewActivity.class);
                startActivity(intent);
            }
        });
        TextView gView = (TextView) findViewById(R.id.textView3);
        gView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, GridViewActivity.class);
                startActivity(intent);
            }
        });
        TextView rView = (TextView) findViewById(R.id.textView4);
        rView.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent intent = new Intent(MainActivity.this, RelativeViewActivity.class);
                startActivity(intent);
            }
        });
    }
}
