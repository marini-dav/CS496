package com.example.sammy.cs496_androidui;

        import android.support.v7.app.AppCompatActivity;
        import android.os.Bundle;
        import android.widget.ArrayAdapter;
        import android.widget.GridView;

        import java.util.ArrayList;

public class GridViewActivity extends AppCompatActivity {
    private ArrayList<Integer> numbers = new ArrayList<>();

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity3);

        for(int i=1; i<=5; i++){
            numbers.add(i);
        }

        GridView gridview = (GridView) findViewById(R.id.grid_view_id);
        ArrayAdapter<Integer> adapter = new ArrayAdapter<>(this,android.R.layout.simple_list_item_1,numbers);
        gridview.setNumColumns(2);
        gridview.setAdapter(adapter);
    }
}
