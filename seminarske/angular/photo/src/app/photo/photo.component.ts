import {Component, OnInit} from '@angular/core';
import {Photo} from '../photo';
import {PhotoService} from '../photo.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-photo',
  templateUrl: './photo.component.html',
  styleUrls: ['./photo.component.css']
})
export class PhotoComponent implements OnInit {

  photo: Photo = {"_id": "", "name": "", "path": "", "views": 0, "likes": 0};
  photoHost = PhotoService.photoHost;


  constructor(private photoService: PhotoService, private route: ActivatedRoute) {
  }

  getPhoto(_id: string): void {
    this.photoService.getPhoto(_id).subscribe(photo => this.photo = photo);
  }

  likePhoto(): void {
    this.photo.likes++;
    this.photoService.updatePhoto(this.photo).subscribe(photo => this.photo = photo);
  }

  ngOnInit() {
    this.route.params.subscribe(params => this.getPhoto(params['_id']));
  }
}
