package com.example.sammy.cs496_androidui;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import java.util.ArrayList;

public class VerticalViewActivity extends AppCompatActivity {
        private ArrayList<Integer> numbers = new ArrayList<>();

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);

            for(int i = 1; i<=5; i++) {
                numbers.add(i);
            }

            TextView vertView = (TextView) findViewById(R.id.vert_view_id);
            vertView.setText((CharSequence) numbers);
        }
    }
