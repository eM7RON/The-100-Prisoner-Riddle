use arrayref::array_ref;
use rand::{seq::SliceRandom, thread_rng};
use rayon::prelude::*;
use std::collections::HashMap;
use std::time::Instant;

fn create_game() -> [[u32; 10]; 10] {
    let mut numbers: Vec<u32> = (1..=100).collect();
    numbers.shuffle(&mut thread_rng());

    let mut game = [[0; 10]; 10];
    for (i, chunk) in numbers.chunks(10).enumerate() {
        game[i].copy_from_slice(chunk);
    }
    
    game
}

fn get_index(lookup: &HashMap<u32, (usize, usize)>, n: u32) -> (usize, usize) {
    *lookup.get(&n).unwrap()
}

fn play(lookup: &HashMap<u32, (usize, usize)>) -> u32 {
    let game = create_game();

    for prisoner in 1..=100 {
        let mut current_number = prisoner;
        let mut loop_size = 1;

        loop {
            let (x, y) = get_index(&lookup, current_number);
            let number_in_box = game[x][y];

            if number_in_box == prisoner {
                break;
            }

            loop_size += 1;

            if loop_size > 50 {
                return 0;
            }

            current_number = number_in_box;
        }
    }

    1
}

fn main() {
    let n = 10_000_000;

    let boxes: [[u32; 10]; 10] = (1..=100)
        .collect::<Vec<_>>()
        .chunks(10)
        .map(|chunk| *array_ref![chunk, 0, 10])
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();

    let mut lookup = HashMap::new();
    for (i, row) in boxes.iter().enumerate() {
        for (j, &num) in row.iter().enumerate() {
            lookup.insert(num, (i, j));
        }
    }

    let start = Instant::now();

    let results: Vec<u32> = (0..n).into_par_iter().map(|_| play(&lookup)).collect();

    let duration = start.elapsed();

    let percentage_success = results.iter().sum::<u32>() as f64 / results.len() as f64 * 100.0;

    println!("{} runs in {:?} seconds\n{:.5}% succeeded", n, duration.as_secs(), percentage_success);
}
